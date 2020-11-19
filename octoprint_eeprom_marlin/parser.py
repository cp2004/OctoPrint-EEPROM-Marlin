# -*- coding: utf-8 -*-
"""
Provide methods for parsing printer communication, specific to this plugin
"""
import re

from octoprint_eeprom_marlin import data

# Bunch of regexes that are useful for parsing
# Some of these are borrowed straight out of OctoPrint's comm layer
# I didn't import them just in case they get renamed/modified in
# future versions, breaking the plugin in the process.
regex_float_pattern = r"[-+]?[0-9]*\.?[0-9]+"
regex_positive_float_pattern = r"[+]?[0-9]*\.?[0-9]+"
regex_int_pattern = r"\d+"

regexes_parameters = {
    "floatX": re.compile(r"(^|[^A-Za-z])[Xx](?P<value>[-+]?[0-9]*\.?[0-9]+)"),
    "floatY": re.compile(r"(^|[^A-Za-z])[Yy](?P<value>%s)" % regex_float_pattern),
    "floatZ": re.compile(r"(^|[^A-Za-z])[Zz](?P<value>%s)" % regex_float_pattern),
    "floatE": re.compile(r"(^|[^A-Za-z])[Ee](?P<value>%s)" % regex_float_pattern),
    "floatF": re.compile(r"(^|[^A-Za-z])[Ff](?P<value>%s)" % regex_float_pattern),
    "floatP": re.compile(r"(^|[^A-Za-z])[Pp](?P<value>%s)" % regex_float_pattern),
    "floatR": re.compile(r"(^|[^A-Za-z])[Rr](?P<value>%s)" % regex_float_pattern),
    "floatT": re.compile(r"(^|[^A-Za-z])[Tt](?P<value>%s)" % regex_float_pattern),
    "floatL": re.compile(r"(^|[^A-Za-z])[Ll](?P<value>%s)" % regex_float_pattern),
    "floatS": re.compile(r"(^|[^A-Za-z])[Ss](?P<value>%s)" % regex_float_pattern),
    "floatA": re.compile(r"(^|[^A-Za-z])[Aa](?P<value>%s)" % regex_float_pattern),
    "floatB": re.compile(r"(^|[^A-Za-z])[Bb](?P<value>%s)" % regex_float_pattern),
    "floatC": re.compile(r"(^|[^A-Za-z])[Cc](?P<value>%s)" % regex_float_pattern),
    "floatK": re.compile(r"(^|[^A-Za-z])[Kk](?P<value>%s)" % regex_float_pattern),
    "floatI": re.compile(r"(^|[^A-Za-z])[Ii](?P<value>%s)" % regex_float_pattern),
    "floatD": re.compile(r"(^|[^A-Za-z])[Dd](?P<value>%s)" % regex_float_pattern),
    "intN": re.compile(r"(^|[^A-Za-z])[Nn](?P<value>%s)" % regex_int_pattern),
    "intS": re.compile(r"(^|[^A-Za-z])[Ss](?P<value>%s)" % regex_int_pattern),
    "intT": re.compile(r"(^|[^A-Za-z])[Tt](?P<value>%s)" % regex_int_pattern),
    "intD": re.compile(r"(^|[^A-Za-z])[Dd](?P<value>%s)" % regex_int_pattern),
}

regex_command = re.compile(r"echo:\s(?P<gcode>M(?P<value>\d{1,3}))")


class Parser:
    def parse_eeprom_data(self, logger, line):
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
            logger.error("Unrecognised EEPROM output line, could not parse")
            logger.error("Line: {}".format(line))
            return

        # work out what values we have
        parameters = {}
        for param in params:
            try:
                param_match = regexes_parameters["float{}".format(param)].search(line)
            except KeyError:
                logger.error("Unrecognised EEPROM command parameter, could not parse")
                logger.error("Parameter: {}".format(param))
                return
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
