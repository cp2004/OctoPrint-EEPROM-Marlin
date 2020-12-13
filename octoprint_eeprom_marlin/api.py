# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from copy import deepcopy

import flask
import octoprint.util

from octoprint_eeprom_marlin.backup import BackupMissingError, BackupNameTakenError
from octoprint_eeprom_marlin.util import build_backup_name, construct_command

CMD_LOAD = "load"
CMD_SAVE = "save"
CMD_BACKUP = "backup"
CMD_RESTORE = "restore"
CMD_RESET = "reset"
CMD_DELETE = "delete"


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
            old_eeprom = deepcopy(self._eeprom_data.to_dict())
            self._eeprom_data.from_list(data.get("eeprom_data"))
            new_eeprom = self._eeprom_data.to_dict()
            self.save_eeprom_data(old_eeprom, new_eeprom)

        elif command == CMD_BACKUP:
            # Execute a backup
            return self.create_backup(data.get("name"))
        elif command == CMD_RESTORE:
            # Restore the backup
            return self.restore_backup(data.get("name"))
        elif command == CMD_DELETE:
            # Delete the backup
            return self.delete_backup(data.get("name"))
        elif command == CMD_RESET:
            # Reset (M502)
            raise NotImplementedError

    def on_api_get(self, request):
        return flask.jsonify(
            {
                "info": self._firmware_info.to_dict(),
                "eeprom": self._eeprom_data.to_dict(),
                "backups": self._backup_handler.get_backups(quick=True),
            }
        )

    def save_eeprom_data(self, old, new):
        if self._printer.is_ready():
            commands = []
            for name, data in old.items():
                new_data = new[name]
                diff = octoprint.util.dict_minimal_mergediff(data, new_data)
                if diff:
                    commands.append(construct_command(new_data))

            if commands:
                self._printer.commands(commands)
                self._printer.commands("M500")

    def create_backup(self, name):
        if not name:
            # Custom backup names should be passed, otherwise auto-generate
            name = build_backup_name()

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
        eeprom_list = []
        for key in eeprom_data.keys():
            eeprom_list.append(
                {
                    "name": key,
                    "command": eeprom_data[key]["command"],
                    "params": eeprom_data[key]["params"],
                }
            )

        # Save the data
        old_data = deepcopy(self._eeprom_data.to_dict())
        self._eeprom_data.from_list(eeprom_list)
        new_data = self._eeprom_data.to_dict()
        self.save_eeprom_data(old_data, new_data)

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
