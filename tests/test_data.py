"""
Tests for the data processing and storage part of the plugin
"""

import unittest
from unittest import mock

from octoprint_eeprom_marlin import data, parser


class DataTestCase(unittest.TestCase):
    def test_individual_data_from_to_dict(self):
        logger = mock.Mock()
        eeprom_parser = parser.Parser(logger)

        # Setup an example steps data class
        data_class = data.IndividualData(
            "steps", "M92", data.ALL_DATA_STRUCTURE["steps"]["params"]
        )

        line = "echo: M92 X80.0 Y80.0 Z800.0 E90.0"
        parsed_data = eeprom_parser.parse_eeprom_data(line)

        data_class.params_from_dict(parsed_data["params"])

        self.assertEqual(
            data_class.params_to_dict(), {"X": 80.0, "Y": 80.0, "Z": 800.0, "E": 90.0}
        )

    def test_data_class(self):
        plugin = mock.Mock()  # mocks the logger that's used in data
        eeprom_parser = parser.Parser(plugin)

        data_class = data.EEPROMData(plugin)

        # Simple one first
        line = "echo: M92 X80.0 Y80.0 Z800.0 E90.0"
        parsed_data = eeprom_parser.parse_eeprom_data(line)
        data_class.from_dict(parsed_data)

        self.assertEqual(
            data_class.to_dict()["steps"],
            {"command": "M92", "params": {"X": 80.0, "Y": 80.0, "Z": 800.0, "E": 90.0}},
        )

        # Now a switched one
        line = "echo: M913 I1 Z164"
        parsed_data = eeprom_parser.parse_eeprom_data(line)
        data_class.from_dict(parsed_data)

        # print(data_class.to_dict()["tmc_hybrid"])

        self.assertEqual(
            data_class.to_dict()["tmc_hybrid"],
            {
                "command": "M913",
                "params": {"I1": {"E": None, "X": None, "Y": None, "Z": 164.0}},
            },
        )

        line = "echo:  M913 T0 E19"
        parsed_data = eeprom_parser.parse_eeprom_data(line)
        data_class.from_dict(parsed_data)

        self.assertEqual(
            data_class.to_dict()["tmc_hybrid"],
            {
                "command": "M913",
                "params": {
                    "I1": {"X": None, "Y": None, "Z": 164, "E": None},
                    "T0": {"X": None, "Y": None, "Z": None, "E": 19},
                },
            },
        )

        line = "echo:  M913 X229 Y229 Z164"
        parsed_data = eeprom_parser.parse_eeprom_data(line)
        data_class.from_dict(parsed_data)

        self.assertEqual(
            data_class.to_dict()["tmc_hybrid"],
            {
                "command": "M913",
                "params": {
                    "I1": {"X": None, "Y": None, "Z": 164, "E": None},
                    "T0": {"X": None, "Y": None, "Z": None, "E": 19.0},
                    "X": 229,
                    "Y": 229,
                    "Z": 164,
                },
            },
        )

    def test_kitchen_sink(self):
        sink = """
            ; @MMcLure
            echo:  G21    ; Units in mm (mm)
            echo:  M149 C ; Units in Celsius
            echo:; Filament settings: Disabled
            echo:  M200 S0 D1.7500
            echo:; Steps per unit:
            echo: M92 X200.0000 Y200.0000 Z400.0000 E415.0000
            echo:; Maximum feedrates (units/s):
            echo:  M203 X400.0000 Y400.0000 Z8.0000 E50.0000
            echo:; Maximum Acceleration (units/s2):
            echo:  M201 X2000.0000 Y2000.0000 Z100.0000 E10000.0000
            echo:; Acceleration (units/s2): P<print_accel> R<retract_accel> T<travel_accel>
            echo:  M204 P800.0000 R10000.0000 T2000.0000
            echo:; Advanced: B<min_segment_time_us> S<min_feedrate> T<min_travel_feedrate> X<max_x_jerk> Y<max_y_jerk> Z<max_z_jerk> E<max_e_jerk>
            echo:  M205 B20000.0000 S0.0000 T0.0000 X8.0000 Y8.0000 Z0.3000 E5.0000
            echo:; Home offset:
            echo:  M206 X0.0000 Y0.0000 Z0.0000
            echo:; Unified Bed Leveling:
            echo:  M420 S1 Z10.0000
            Unified Bed Leveling System v1.01 active
            echo:; Active Mesh Slot: 0
            echo:; EEPROM can hold 3 meshes.
            echo:; Material heatup parameters:
            echo:  M145 S0 H190.0000 B60.0000 F0
            echo:  M145 S1 H210.0000 B70.0000 F0
            echo:; PID settings:
            echo:  M301 P19.0986 I1.3998 D65.1453
            echo:  M304 P46.3000 I9.0700 D157.5700
            echo:; Z-Probe Offset (mm):
            echo:  M851 X-29.0000 Y1.0000 Z-1.9250
            echo:; Stepper driver current:
            echo:  M906 X1200 Y1200 Z400
            echo:  M906 I1 Z400
            echo:  M906 T0 E900
            echo:; Driver stepping mode:
            echo:  M569 S1 X Y Z
            echo:  M569 S1 I1 Z
            echo:; Linear Advance:
            echo:  M900 K0.0400
            echo:; Filament load/unload lengths:
            echo:  M603 L25.0000 U75.0000
            echo:; Filament runout sensor:
            echo:  M412 S0
            ok P63 B31
            """

        plugin = mock.Mock()  # mocks the logger that's used in data
        eeprom_parser = parser.Parser(plugin)
        eeprom_data = data.EEPROMData(plugin)

        for line in sink.splitlines():
            parsed_data = eeprom_parser.parse_eeprom_data(line.strip())
            if parsed_data:
                eeprom_data.from_dict(parsed_data)

        result = eeprom_data.to_dict()

        # Some randomly sampled expected results
        expected = {
            "steps": {
                "command": "M92",
                "params": {
                    "X": 200.0,
                    "Y": 200.0,
                    "Z": 400.0,
                    "E": 415.0,
                },
            },
            "tmc_current": {
                "command": "M906",
                "params": {
                    "X": 1200,
                    "Y": 1200,
                    "Z": 400,
                    "E": None,
                    "I1": {"E": None, "X": None, "Y": None, "Z": 400.0},
                    "T0": {"E": 900.0, "X": None, "Y": None, "Z": None},
                },
            },
        }

        self.assertEqual(result["steps"], expected["steps"])
        self.assertEqual(result["tmc_current"], expected["tmc_current"])
