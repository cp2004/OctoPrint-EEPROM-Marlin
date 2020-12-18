# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = (
    "Copyright (C) 2020 Charlie Powell - Released under terms of the AGPLv3 License"
)
from copy import deepcopy

import flask
import octoprint.util

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
        self._settings = plugin._settings
        self._logger = plugin._logger
        self._printer = plugin._printer
        self._firmware_info = plugin._firmware_info
        self._eeprom_data = plugin._eeprom_data
        self._backup_handler = plugin._backup_handler
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
            # Get data from printer
            if self._printer.is_ready():
                self._printer.commands(
                    "M503" if self._settings.get(["use_m503"]) else "M501"
                )
        elif command == CMD_SAVE:
            # Send changed data to printer
            self.save_eeprom_data(data.get("eeprom_data"))

        elif command == CMD_BACKUP:
            # Execute a backup
            return self.create_backup(data.get("name"))
        elif command == CMD_RESTORE:
            # Restore the backup
            return self.restore_backup(data.get("name"))
        elif command == CMD_DELETE:
            # Delete the backup
            return self.delete_backup(data.get("name"))
        elif command == CMD_UPLOAD_RESTORE:
            # Restore backup from upload
            return self.upload_restore(data.get("data"))
        elif command == CMD_RESET:
            # Reset (M502)
            return self.reset_eeprom()

    def on_api_get(self, request):
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
                self._printer.commands(commands)
                self._printer.commands("M500")

    def reset_eeprom(self):
        if self._printer.is_ready():
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

        eeprom_data = self._eeprom_data.to_dict()
        try:
            self._backup_handler.create_backup(name, eeprom_data)
            success = True
            error = ""
        except BackupNameTakenError:
            success = False
            error = "Backup name is already in use, please use a different name"
        except Exception as e:
            success = False
            error = "An unknown error occured while creating the backup, consult the log for details"
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
        except Exception:
            response = {
                "success": False,
                "error": "Unknown error occurred, check log for details",
            }

        response.update({"backups": self._backup_handler.get_backups(quick=True)})

        return flask.jsonify(response)

    def upload_restore(self, backup_data):
        if not self._backup_handler._perform_validate(backup_data):
            return flask.jsonify(
                {"success": False, "error": "Backup is not valid, could not restore it"}
            )

        eeprom_data = backup_data["data"]
        eeprom_list = util.backup_json_to_list(eeprom_data)

        self.save_eeprom_data(eeprom_list)
        return flask.jsonify({"success": True, "eeprom": self._eeprom_data.to_dict()})
