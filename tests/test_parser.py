import unittest
from unittest import mock

from octoprint_eeprom_marlin import parser


class ParserTestCase(unittest.TestCase):
    def test_regex_command(self):
        test_cases_command = {
            "echo: M92 X80.0 Y80.0 Z800.0 E90.0": "M92",
            "echo: M203 X400.0 Y400.0 Z5.0 E25.0": "M203",
            "echo: M201 E74.0 X2000.0 Y2000.0 Z10.0": "M201",
        }

        for test, result in test_cases_command.items():
            match = parser.regex_command.match(test)
            self.assertEqual(match.group("gcode"), result)

    def test_regex_params(self):
        test_cases_params = {
            "echo: M92 X80.0 Y80.0 Z800.0 E90.0": {
                "params": ["X", "Y", "Z", "E"],
                "results": {"X": "80.0", "Y": "80.0", "Z": "800.0", "E": "90.0"},
            },
            "echo: M203 X400.0 Y400.0 Z5.0 E25.0": {
                "params": ["X", "Y", "Z", "E"],
                "results": {"X": "400.0", "Y": "400.0", "Z": "5.0", "E": "25.0"},
            },
            "echo: M201 E74.0 X2000.0 Y2000.0 Z10.0": {
                "params": ["X", "Y", "Z", "E"],
                "results": {"X": "2000.0", "Y": "2000.0", "Z": "10.0", "E": "74.0"},
            },
        }
        for test, result in test_cases_params.items():
            matches = parser.regex_parameter.findall(test)
            for match in matches:
                if match[0] in result["params"]:
                    self.assertEqual(match[1], result["results"][match[0]])

    def test_parser(self):
        # Lets throw the entire M503 response at it, line by line...
        logger = mock.Mock()
        m503_response = {
            "echo:; Steps per unit:": None,
            "echo: M92 X80.0 Y80.0 Z800.0 E90.0": {
                "name": "steps",
                "command": "M92",
                "params": {"X": 80.0, "Y": 80.0, "Z": 800.0, "E": 90.0},
            },
            "echo:; Maximum feedrates (units/s):": None,
            "echo: M203 X400.0 Y400.0 Z5.0 E25.0": {
                "name": "feedrate",
                "command": "M203",
                "params": {"X": 400.0, "Y": 400.0, "Z": 5.0, "E": 25.0},
            },
            "echo:; Maximum Acceleration (units/s2):": None,
            "echo:  M201 E74.0 X2000.0 Y2000.0 Z10.0": {
                "name": "max_acceleration",
                "command": "M201",
                "params": {"X": 2000.0, "Y": 2000.0, "Z": 10.0, "E": 74.0},
            },
            "echo:; Acceleration (units/s2): P<print_accel> R<retract_accel> T<travel_accel>": None,
            "echo: M204 P850.0 R1000.0 T300.0 S300.0": {
                "name": "print_acceleration",
                "command": "M204",
                "params": {"P": 850.0, "R": 1000.0, "T": 300.0},
            },
            "echo:; Home offset:": None,
            "echo: M206 X0.0 Y0.0 Z0.0": {
                "name": "home_offset",
                "command": "M206",
                "params": {"X": 0.0, "Y": 0.0, "Z": 0.0},
            },
            "echo:; Z-Probe Offset (mm):": None,
            "echo:  M851 X5.0 Y5.0 Z0.2": {
                "name": "probe_offset",
                "command": "M851",
                "params": {"X": 5.0, "Y": 5.0, "Z": 0.2},
            },
            "echo:; Filament settings: Disabled": None,
            "echo: M200 D1.75 S0": {
                "name": "filament",
                "command": "M200",
                "params": {"D": 1.75},
            },
            "echo:; Enstop adjustment:": None,
            "echo: M666 X-1.0 Y0.0 Z0.0": {
                "name": "endstop",
                "command": "M666",
                "params": {"X": -1.0, "Y": 0.0, "Z": 0.0},
            },
            "echo:; Delta config:": None,
            "echo:  M665 B0.0 H100.0 L25.0 R6.5 S100.0 X20.0 Y20.0 Z20.0": {
                "name": "delta",
                "command": "M665",
                "params": {
                    "B": 0.0,
                    "H": 100.0,
                    "L": 25.0,
                    "R": 6.5,
                    "S": 100.0,
                    "X": 20.0,
                    "Y": 20.0,
                    "Z": 20.0,
                },
            },
            "echo:; Bed Levelling:": None,
            "echo: M420 S1.0 Z0.0": {
                "name": "autolevel",
                "command": "M420",
                "params": {"S": True, "Z": 0.0},
            },
            "echo:; Linear Advance:": None,
            "echo: M900 K0.01": {
                "name": "linear",
                "command": "M900",
                "params": {"K": 0.01},
            },
            "echo:; Advanced: B<min_segment_time_us> S<min_feedrate> T<min_travel_feedrate> X<max_x_jerk> Y<max_y_jerk> Z<max_z_jerk> E<max_e_jerk>": None,
            "echo: M205 B19999.9 S0.0 T0.0 X10.0 Y10.0 Z0.3 E5.0 J0.0": {
                "name": "advanced",
                "command": "M205",
                "params": {
                    "S": 0.0,
                    "T": 0.0,
                    "B": 19999.9,
                    "X": 10.0,
                    "Y": 10.0,
                    "Z": 0.3,
                    "E": 5.0,
                    "J": 0.0,
                },
            },
            "echo:; Material heatup parameters:": None,
            "echo: M145 S0 B60.0 F255.0 H199.0": {
                "name": "material",
                "command": "M145",
                "params": {"S": 0, "B": 60.0, "H": 199.0, "F": 255.0},
            },
            "echo: M145 S1 B75.0 F0.0 H240.0": {
                "name": "material",
                "command": "M145",
                "params": {"S": 1, "B": 75.0, "H": 240.0, "F": 0.0},
            },
            "echo:; Hotend PID settings:": None,
            "echo: M301 P30.5 I2.51 D73.09": {
                "name": "hotend_pid",
                "command": "M301",
                "params": {"P": 30.5, "I": 2.51, "D": 73.09},
            },
            "echo:; Bed PID settings:": None,
            "echo: M304 P131.06 I11.79 D971.23": {
                "name": "bed_pid",
                "command": "M304",
                "params": {"P": 131.06, "I": 11.79, "D": 971.23},
            },
            "echo: M900 T1 K1.50": {
                "name": "linear",
                "command": "M900",
                "params": {"K": 1.5, "T": 1},
            },
            "echo:  M913 X229 Y229 Z164": {
                "name": "tmc_hybrid",
                "command": "M913",
                "params": {"X": 229, "Y": 229, "Z": 164},
            },
            "echo:  M913 I1 Z164": {
                "name": "tmc_hybrid",
                "command": "M913",
                "params": {"I": 1, "Z": 164},
            },
            "echo:  M913 T0 E19": {
                "name": "tmc_hybrid",
                "command": "M913",
                "params": {"T": 0, "E": 19},
            },
        }

        eeprom_parser = parser.Parser(logger)
        for line, expected_result in m503_response.items():
            self.assertEqual(eeprom_parser.parse_eeprom_data(line), expected_result)
