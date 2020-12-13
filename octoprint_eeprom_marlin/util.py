# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import time


def build_backup_name():
    return "eeprom_backup-{}".format(time.strftime("%Y%m%d-%H%M%S"))


def construct_command(data):
    command = data["command"]
    for param, value in data["params"].items():
        value = str(value) if command != "M145" and param != "S" else str(int(value))
        command = command + " " + param + value
    return command


def backup_json_to_list(eeprom_data):
    eeprom_list = []
    for key in eeprom_data.keys():
        eeprom_list.append(
            {
                "name": key,
                "command": eeprom_data[key]["command"],
                "params": eeprom_data[key]["params"],
            }
        )

    return eeprom_list
