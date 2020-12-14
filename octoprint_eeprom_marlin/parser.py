# -*- coding: utf-8 -*-
"""
Provide methods for parsing printer communication, specific to this plugin
"""
from __future__ import absolute_import, division, unicode_literals

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
        :param logger: plugin's logging instance
        :param line: line received from FW
        :return: dict: parsed values
        """

        # work out what command we have
        command_match = regex_command.match(line)
        if command_match:
            command = command_match.group("gcode")
        else:
            return

        # grab parameters that we can look at
        try:
            params = data.COMMAND_PARAMS[command]
        except KeyError:
            self._logger.error("Unrecognised EEPROM output line, could not parse")
            self._logger.error("Line: {}".format(line))
            return

        # work out what values we have
        parameters = {}
        for param in params:
            try:
                param_match = regexes_parameters["float{}".format(param)].search(line)
            except KeyError:
                self._logger.error(
                    "Unrecognised EEPROM command parameter, could not parse"
                )
                self._logger.error("Parameter: {}".format(param))
                continue
            if param_match:
                parameters[param] = float(param_match.group("value"))

        # construct response
        return {
            "name": data.COMMAND_NAMES[command],
            "command": command,
            "params": parameters,
        }

    @staticmethod
    def is_marlin(name):
        return "marlin" in name.lower()
