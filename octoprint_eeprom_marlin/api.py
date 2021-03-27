# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = (
    "Copyright (C) 2020 Charlie Powell - Released under terms of the AGPLv3 License"
)
from copy import deepcopy

import flask
import octoprint.util

from octoprint.access.permissions import Permissions
from octoprint.access import ADMIN_GROUP, USER_GROUP, READONLY_GROUP

from octoprint_eeprom_marlin import util
from octoprint_eeprom_marlin.backup import BackupMissingError, BackupNameTakenError

CMD_LOAD = "load"
CMD_SAVE = "save"
CMD_BACKUP = "backup"
CMD_RESTORE = "restore"
CMD_RESET = "reset"
CMD_DELETE = "delete"
CMD_UPLOAD_RESTORE = "upload_restore"


class API:
    def __init__(self, plugin):
        self._settings = plugin._settings  # noqa
        self._logger = plugin._logger  # noqa
        self._printer = plugin._printer  # noqa
        self._firmware_info = plugin._firmware_info  # noqa
        self._eeprom_data = plugin._eeprom_data  # noqa
        self._backup_handler = plugin._backup_handler  # noqa
        self._plugin = plugin

    @staticmethod
    def get_api_commands():
        return {
            CMD_LOAD: [],
            CMD_SAVE: ["eeprom_data"],
            CMD_BACKUP: [],
            CMD_RESTORE: ["name"],
            CMD_DELETE: ["name"],
            CMD_RESET: [],
            CMD_UPLOAD_RESTORE: ["data"],
        }

    def on_api_command(self, command, data):
        if command == CMD_LOAD:
            if not Permissions.PLUGIN_EEPROM_MARLIN_READ.can():
                # Insufficient rights
                flask.abort(403)

            # Get data from printer
            if self._printer.is_ready():
                self._printer.commands(
                    "M503" if self._settings.get(["use_m503"]) else "M501"
                )
        elif command == CMD_SAVE:
            if not Permissions.PLUGIN_EEPROM_MARLIN_EDIT.can():
                # Insufficient rights
                flask.abort(403)

            # Send changed data to printer
            self.save_eeprom_data(data.get("eeprom_data"))

        elif command == CMD_BACKUP:
            if not Permissions.PLUGIN_EEPROM_MARLIN_EDIT.can():
                # Insufficient rights
                flask.abort(403)

            # Execute a backup
            return self.create_backup(data.get("name"))
        elif command == CMD_RESTORE:
            if not Permissions.PLUGIN_EEPROM_MARLIN_EDIT.can():
                # Insufficient rights
                flask.abort(403)

            # Restore the backup
            return self.restore_backup(data.get("name"))
        elif command == CMD_DELETE:
            if not Permissions.PLUGIN_EEPROM_MARLIN_EDIT.can():
                # Insufficient rights
                flask.abort(403)

            # Delete the backup
            return self.delete_backup(data.get("name"))
        elif command == CMD_UPLOAD_RESTORE:
            if not Permissions.PLUGIN_EEPROM_MARLIN_EDIT.can():
                # Insufficient rights
                flask.abort(403)

            # Restore backup from upload
            return self.upload_restore(data.get("data"))
        elif command == CMD_RESET:
            if not Permissions.PLUGIN_EEPROM_MARLIN_RESET.can():
                # Insufficient rights
                flask.abort(403)

            # Reset (M502)
            return self.reset_eeprom()

    def on_api_get(self, request):
        if not Permissions.PLUGIN_EEPROM_MARLIN_READ.can():
            flask.abort(403)

        return flask.jsonify(
            {
                "info": self._firmware_info.to_dict(),
                "eeprom": self._eeprom_data.to_dict(),
                "backups": self._backup_handler.get_backups(quick=True),
            }
        )

    def save_eeprom_data(self, new_data):
        old_eeprom = deepcopy(self._eeprom_data.to_dict())
        self._eeprom_data.from_list(new_data)
        new_eeprom = self._eeprom_data.to_dict()
        if self._printer.is_ready():
            commands = []
            for name, data in old_eeprom.items():
                new_data = new_eeprom[name]
                diff = octoprint.util.dict_minimal_mergediff(data, new_data)
                if diff:
                    commands.append(util.construct_command(new_data))

            if commands:
                self._logger.info("Saving EEPROM data")
                self._logger.info("Commands to send: {}".format(commands))
                self._printer.commands(commands)
                self._printer.commands("M500")

    def reset_eeprom(self):
        if self._printer.is_ready():
            self._logger.info("Resetting EEPROM on API request")
            # Reset, save, load
            self._printer.commands(
                ["M502", "M500", "M503" if self._settings.get(["use_m503"]) else "M501"]
            )

    def create_backup(self, name):
        if not name:
            # Custom backup names should be passed, otherwise auto-generate
            name = util.build_backup_name()
        else:
            name = util.sanitize(name)
            if not name:
                # Name consisted of only symbols or something, no empty names around here
                name = util.build_backup_name()

        self._logger.info("Creating backup {}".format(name))

        eeprom_data = self._eeprom_data.to_dict()
        try:
            self._backup_handler.create_backup(name, eeprom_data)
            success = True
            error = ""
        except BackupNameTakenError:
            success = False
            error = "Backup name is already in use, please use a different name"
            self._logger.error(error)
        except Exception as e:
            success = False
            error = "An unknown error occurred while creating the backup, please consult the log for details"
            self._logger.exception(e)

        return flask.jsonify({"success": success, "error": error})

    def restore_backup(self, name):
        if not self._printer.is_ready():
            return flask.abort(409)

        try:
            backup_data = self._backup_handler.read_backup(name)
        except BackupMissingError as e:
            self._logger.error("Specified backup could not be found")
            self._logger.exception(e)
            return flask.jsonify(
                {"success": False, "error": "Backup specified does not exist"}
            )

        self._logger.info("Restoring backup from {}".format(name))

        eeprom_data = backup_data["data"]
        # convert json dict to a list, for usage of common parsing methods
        eeprom_list = util.backup_json_to_list(eeprom_data)

        # Save the data
        self.save_eeprom_data(eeprom_list)

        return flask.jsonify(
            {"success": True, "eeprom": self._eeprom_data.to_dict(), "name": name}
        )

    def delete_backup(self, name):
        try:
            self._backup_handler.delete_backup(name)
            response = {"success": True}
        except BackupMissingError:
            response = {
                "success": False,
                "error": "The backup specified could not be found",
            }
            self._logger.error("Backup at {} could not be found".format(name))
        except Exception as e:
            response = {
                "success": False,
                "error": "Unknown error occurred, check log for details",
            }
            self._logger.exception(e)

        response.update({"backups": self._backup_handler.get_backups(quick=True)})

        return flask.jsonify(response)

    def upload_restore(self, backup_data):
        if not self._backup_handler._perform_validate(backup_data):
            error = "Backup is not valid, could not restore it"
            self._logger.error(error)
            return flask.jsonify({"success": False, "error": error})

        eeprom_data = backup_data["data"]
        eeprom_list = util.backup_json_to_list(eeprom_data)

        self.save_eeprom_data(eeprom_list)
        self._logger.info("Restored from uploaded backup")
        return flask.jsonify({"success": True, "eeprom": self._eeprom_data.to_dict()})
