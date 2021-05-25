# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

"""
Provide methods for parsing printer communication, specific to this plugin
"""
__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = (
    "Copyright (C) 2020 Charlie Powell - Released under terms of the AGPLv3 License"
)

import re

from octoprint_eeprom_marlin import data

# Bunch of regexes that are useful for parsing
# Some of these are borrowed straight out of OctoPrint's comm layer
# I didn't import them just in case they get renamed/modified in
# future versions, breaking the plugin in the process.
regex_float_pattern = r"[-+]?[0-9]*\.?[0-9]+"
regex_positive_float_pattern = r"[+]?[0-9]*\.?[0-9]+"
regex_int_pattern = r"\d+"


def regex_creator(value_type, param_letter):
    value_pattern = regex_float_pattern if value_type == "float" else regex_int_pattern
    letter = param_letter.upper() + param_letter.lower()
    return re.compile(r"(^|[^A-Za-z])[%s](?P<value>%s)" % (letter, value_pattern))


regexes_parameters = {
    "floatA": regex_creator("float", "A"),
    "floatB": regex_creator("float", "B"),
    "floatC": regex_creator("float", "C"),
    "floatD": regex_creator("float", "D"),
    "floatE": regex_creator("float", "E"),
    "floatF": regex_creator("float", "F"),
    "floatH": regex_creator("float", "H"),
    "floatI": regex_creator("float", "I"),
    "floatJ": regex_creator("float", "J"),
    "floatK": regex_creator("float", "K"),
    "floatL": regex_creator("float", "L"),
    "floatP": regex_creator("float", "P"),
    "floatR": regex_creator("float", "R"),
    "floatS": regex_creator("float", "S"),
    "floatT": regex_creator("float", "T"),
    "floatU": regex_creator("float", "U"),
    "floatX": regex_creator("float", "X"),
    "floatY": regex_creator("float", "Y"),
    "floatZ": regex_creator("float", "Z"),
}

regex_command = re.compile(r"echo:\s*(?P<gcode>M(?P<value>\d{1,3}))")


class Parser:
    def __init__(self, logger):
        self._logger = logger

    def parse_eeprom_data(self, line):
        """
        Parse a received line from the printer into a dictionary of name, command, params
        Eg: `echo: M92 X80.0 Y80.0 Z800.0 E90.0`
        to {"name": steps, "command": "M92", "params": {
            "X": 80.0,
            "Y": 80.0,
            "Z": 800.0,
            "E": 90.0
        }
        :param line: line received from FW
        :return: dict: parsed values
        """

        # work out what command we have
        command_match = regex_command.match(line)
        if command_match:
            command = command_match.group("gcode")
        else:
            return

        # Find the name (ID) of the command to use internally
        try:
            command_name = data.find_name_from_command(command)
        except ValueError:
            self._logger.warning("EEPROM output line not recognized, skipped")
            self._logger.warning("Line: {}".format(line.strip("\r\n ")))
            return

        # grab parameters that we can look at
        params = data.ALL_DATA_STRUCTURE[command_name]["params"]

        # work out what values we have
        parameters = {}
        for param, param_value in params.items():
            param_match = regexes_parameters["float{}".format(param)].search(line)
            if param_match:
                value = float(param_match.group("value"))
                if param_value["type"] == "bool":
                    value = True if int(value) == 1 else False

                parameters[param] = value

        # construct response
        return {
            "name": command_name,
            "command": command,
            "params": parameters,
        }

    @staticmethod
    def is_marlin(name):
        return "marlin" in name.lower()
