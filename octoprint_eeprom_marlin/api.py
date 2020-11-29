# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from copy import deepcopy

import flask
import octoprint.util

CMD_LOAD = "load"
CMD_SAVE = "save"
CMD_BACKUP = "backup"
CMD_RESTORE = "restore"


class API:
    def __init__(self, plugin):
        self._settings = plugin._settings
        self._logger = plugin._logger
        self._printer = plugin._printer
        self._firmware_info = plugin._firmware_info
        self._eeprom_data = plugin._eeprom_data
        self._plugin = plugin

    @staticmethod
    def get_api_commands():
        return {
            "load": [],
            "save": ["eeprom_data"],
            "backup": [],
            "restore": ["data"],
            "reset": [],
        }

    def on_api_command(self, command, data):
        if command == CMD_LOAD:
            # Get data from printer
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
            raise NotImplementedError
        elif command == CMD_RESTORE:
            # Restore the backup
            raise NotImplementedError

    def on_api_get(self, request):
        return flask.jsonify(
            {
                "info": self._firmware_info.to_dict(),
                "eeprom": self._eeprom_data.to_dict(),
            }
        )

    def save_eeprom_data(self, old, new):
        commands = []
        for name, data in old.items():
            new_data = new[name]
            diff = octoprint.util.dict_minimal_mergediff(data, new_data)
            if diff:
                commands.append(self.construct_command(new_data))

        if commands:
            self._printer.commands(commands)
            self._printer.commands("M500")

    @staticmethod
    def construct_command(data):
        command = data["command"]
        for param, value in data["params"].items():
            value = (
                str(value) if command != "M145" and param != "S" else str(int(value))
            )
            command = command + " " + param + value
        return command
