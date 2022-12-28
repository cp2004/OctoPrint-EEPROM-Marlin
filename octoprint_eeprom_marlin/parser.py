import copy

"""
Provide methods for parsing printer communication, specific to this plugin
"""
__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = (
    "Copyright (C) 2020 Charlie Powell - Released under terms of the AGPLv3 License"
)

import re

from octoprint_eeprom_marlin import data

# Some regexes used for parsing. Initially borrowed from OctoPrint's comm layer
# but modified to suit the plugin better.

regex_float_pattern = r"[-+]?[0-9]*\.?[0-9]+"

regex_parameter = re.compile(r"(?P<letter>[A-Za-z])(?P<value>[-+]?[0-9]*\.?[0-9]+)")
regex_command = re.compile(r"echo:\s*(?P<gcode>M(?P<value>\d{1,3}))")

regex_stats = {
    "prints": re.compile(r"Prints: (\d*)"),
    "finished": re.compile(r"Finished: (\d*)"),
    "failed": re.compile(r"Failed: (\d*)"),
    "total_time": re.compile(r"Total time: (.*),"),
    "longest": re.compile(r"Longest job: (.*)"),
    "filament": re.compile(r"Filament used: (.*m)"),
}


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

        data_structure = data.ALL_DATA_STRUCTURE[command_name]
        params = copy.deepcopy(data_structure["params"])
        if "switches" in data_structure:
            params.update(
                {f"{param}": {"type": "switch"} for param in data_structure["switches"]}
            )

        # work out what values we have
        parameters = {}
        matches = regex_parameter.findall(line)
        for match in matches:
            if match[0] in params.keys():
                # We have a supported parameter
                p = match[0].upper()
                v = float(match[1])

                if params[p]["type"] == "bool":
                    v = True if int(v) == 1 else False
                if params[p]["type"] == "switch":
                    v = int(v)

                parameters[p] = v

        # construct response
        return {
            "name": command_name,
            "command": command,
            "params": parameters,
        }

    @staticmethod
    def is_marlin(name):
        return "marlin" in name.lower()

    @staticmethod
    def parse_stats_line(line):
        # Run all the regexes against the line to grab the params
        stats = {}
        for key, regex in regex_stats.items():
            match = regex.search(line)
            if match:
                stats[key] = match.group(1)

        return stats
