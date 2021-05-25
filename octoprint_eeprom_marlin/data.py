# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = (
    "Copyright (C) 2020 Charlie Powell - Released under terms of the AGPLv3 License"
)
try:
    from typing import Dict, Optional
except ImportError:
    # we don't need these, just for typed comments
    # TODO PY3: Type annotations!
    Dict = Optional = None
    pass


# This defines the data structure used in both the frontend and the backend. Must be kept in sync with
# the observables in the viewmodel. UI will update automatically from this structure using the Jinja templates.
# TODO double check the data types
# float1: 1 decimal place number input
# float2: 2 decimal place number input
# int:    integer input
# bool:   On or off checkbox, maps to 0/1 to send to printer
ALL_DATA_STRUCTURE = {
    "steps": {
        "command": "M92",
        "params": {
            "X": {"type": "float1", "label": "X Steps", "units": "steps/mm"},
            "Y": {"type": "float1", "label": "Y Steps", "units": "steps/mm"},
            "Z": {"type": "float1", "label": "Z Steps", "units": "steps/mm"},
            "E": {"type": "float1", "label": "E Steps", "units": "steps/mm"},
        },
        "name": "Steps",
    },
    "feedrate": {
        "command": "M203",
        "params": {
            "X": {"type": "float1", "label": "X axis", "units": "mm/s"},
            "Y": {"type": "float1", "label": "Y axis", "units": "mm/s"},
            "Z": {"type": "float1", "label": "Z axis", "units": "mm/s"},
            "E": {"type": "float1", "label": "E axis", "units": "mm/s"},
        },
        "name": "Feedrate",
    },
    "max_acceleration": {
        "command": "M201",
        "params": {
            "X": {
                "type": "float1",
                "label": "X maximum acceleration",
                "units": "mm/s2",
            },
            "Y": {
                "type": "float1",
                "label": "Y maximum acceleration",
                "units": "mm/s2",
            },
            "Z": {
                "type": "float1",
                "label": "Z maximum acceleration",
                "units": "mm/s2",
            },
            "E": {
                "type": "float1",
                "label": "E maximum acceleration",
                "units": "mm/s2",
            },
        },
        "name": "Maximum Acceleration",
    },
    "print_acceleration": {
        "command": "M204",
        "params": {
            "P": {"type": "float1", "label": "Printing acceleration", "units": "mm/s2"},
            "R": {"type": "float1", "label": "Retract acceleration", "units": "mm/s2"},
            "T": {"type": "float1", "label": "Travel acceleration", "units": "mm/s2"},
        },
        "name": "Print Acceleration",
    },
    "probe_offset": {
        "command": "M851",
        "params": {
            "X": {"type": "float2", "label": "Z probe X offset", "units": "mm"},
            "Y": {"type": "float2", "label": "Z probe Y offset", "units": "mm"},
            "Z": {"type": "float2", "label": "Z probe Z offset", "units": "mm"},
        },
        "name": "Probe Offset",
    },
    "home_offset": {
        "command": "M206",
        "params": {
            "X": {"type": "float2", "label": "X home offset", "units": "mm"},
            "Y": {"type": "float2", "label": "Y home offset", "units": "mm"},
            "Z": {"type": "float2", "label": "Z home offset", "units": "mm"},
        },
        "name": "Home Offset",
    },
    "endstop": {
        "command": "M666",
        "params": {
            "X": {"type": "float2", "label": "Adjustment for X", "units": "mm"},
            "Y": {"type": "float2", "label": "Adjustment for Y", "units": "mm"},
            "Z": {"type": "float2", "label": "Adjustment for Z", "units": "mm"},
        },
        "name": "Endstop Offsets",
    },
    "delta": {
        "command": "M665",
        "params": {
            "L": {"type": "float2", "label": "Diagonal rod"},
            "R": {"type": "float2", "label": "Delta radius"},
            "H": {"type": "float2", "label": "Delta height"},
            "S": {"type": "float2", "label": "Segments per second"},
            "X": {"type": "float2", "label": "Alpha (Tower 1) angle trim"},
            "Y": {"type": "float2", "label": "Beta (Tower 2) angle trim"},
            "Z": {"type": "float2", "label": "Gamma (Tower 3) angle trim"},
            "A": {"type": "float2", "label": "Alpha (Tower 1) diagonal rod trim"},
            "B": {"type": "float2", "label": "Beta (Tower 2) diagonal rod trim"},
            "C": {"type": "float2", "label": "Gamma (Tower 3) diagonal rod trim"},
        },
        "name": "Delta Configuration",
    },
    "linear": {
        "command": "M900",
        "params": {"K": {"type": "float2", "label": "K factor"}},
        "name": "Linear Advance",
    },
    "filament": {
        "command": "M200",
        "params": {
            "D": {"type": "float2", "label": "Filament Diameter", "units": "mm"}
        },
        "name": "Filament Settings",
    },
    "hotend_pid": {
        "command": "M301",
        "params": {
            "P": {"type": "float2", "label": "Hotend kP"},
            "I": {"type": "float2", "label": "Hotend kI"},
            "D": {"type": "float2", "label": "Hotend kD"},
        },
        "name": "Hotend PID",
    },
    "bed_pid": {
        "command": "M304",
        "params": {
            "P": {"type": "float2", "label": "Bed kP"},
            "I": {"type": "float2", "label": "Bed kI"},
            "D": {"type": "float2", "label": "Bed kD"},
        },
        "name": "Bed PID",
    },
    "advanced": {
        "command": "M205",
        "params": {
            "B": {"type": "float2", "label": "Minimum segment time", "units": "µs"},
            "E": {"type": "float2", "label": "E max jerk", "units": "mm/s"},
            "J": {"type": "float2", "label": "Junction Deviation"},
            "S": {
                "type": "float1",
                "label": "Minimum feedrate for print moves",
                "units": "mm/s",
            },
            "T": {
                "type": "float1",
                "label": "Minimum feedrate for travel moves",
                "units": "mm/s",
            },
            "X": {"type": "float1", "label": "X max jerk", "units": "mm/s"},
            "Y": {"type": "float1", "label": "Y max jerk", "units": "mm/s"},
            "Z": {"type": "float1", "label": "Z max jerk", "units": "mm/s"},
        },
        "name": "Advanced",
    },
    "autolevel": {
        "command": "M420",
        "params": {
            "S": {"type": "bool", "label": "Enabled"},
            "Z": {"type": "float1", "label": "Z fade height", "units": "mm"},
        },
        "name": "Autolevel",
    },
    "material1": {
        "command": "M145",
        "params": {
            "S": {"type": "float1", "label": "Hotend temperature", "units": "°C"},
            "B": {"type": "float1", "label": "Bed temperature", "units": "°C"},
            "F": {"type": "int", "label": "Fan speed", "units": "0-255"},
        },
        "name": "Material Preset (1)",
    },
    "material2": {
        "command": "M145",
        "params": {
            "S": {"type": "float1", "label": "Hotend temperature", "units": "°C"},
            "B": {"type": "float1", "label": "Bed temperature", "units": "°C"},
            "F": {"type": "int", "label": "Fan speed", "units": "0-255"},
        },
        "name": "Material Preset (2)",
    },
    "filament_change": {
        "command": "M603",
        "params": {
            "L": {"type": "float1", "label": "Load length", "units": "mm"},
            "U": {"type": "float1", "label": "Unload length", "units": "mm"},
        },
        "name": "Filament Change",
    },
}


def find_name_from_command(command):
    for key, data in ALL_DATA_STRUCTURE.items():
        if command == data["command"]:
            return key
    else:
        raise ValueError


class FirmwareInfo:
    """
    Holds firmware info data
    """

    name = ""  # type: str
    is_marlin = False  # type: bool
    additional_info = {}  # type: dict
    capabilities = {}  # type: dict

    def additional_info_from_dict(self, data):
        self.additional_info = {}
        for key, value in data.items():
            self.additional_info[key] = value

    def add_capabilities(self, caps):
        for capability, value in caps.items():
            self.capabilities[capability] = value

    def to_dict(self):
        # For sending to UI
        return {
            "name": self.name,
            "is_marlin": self.is_marlin,
            "additional": self.additional_info,
            "capabilities": self.capabilities,
        }


class IndividualData:
    """
    Holding individual data entries
    """

    def __init__(self, name, command, params):
        self.name = name
        self.command = command
        self.params = params
        for param in self.params:
            self.params[param]["value"] = None

    def params_from_dict(self, data):
        for key, value in data.items():
            if value is not None:
                self.params[key]["value"] = value

    def params_to_dict(self):
        # Ready to send to the UI
        params = {}
        for param, data in self.params.items():
            params[param] = data["value"]

        return params

    def generate_command(self):
        command = self.command
        for param, data in self.params.items():
            if data["value"] is None:
                continue
            command += " " + param + data["value"]

        return command


class EEPROMData:
    """
    Holds recieved EEPROM data
    """

    def __init__(self, plugin):
        self.plugin = plugin

        for key, data in ALL_DATA_STRUCTURE.items():
            setattr(self, key, IndividualData(key, data["command"], data["params"]))

        # noinspection PyProtectedMember
        self.plugin._logger.info("EEPROM Data initialised")

    def create_data_structure(self):
        for key, data in ALL_DATA_STRUCTURE.items():
            setattr(self, key, IndividualData(key, data["command"], data["params"]))

    def from_list(self, data):
        """
        Parse data from list into class
        :param data: list of dictionaries to parse
        :return: None
        """
        for item in data:
            self.from_dict(item)

    def from_dict(self, data, ui=True):
        """
        Parse data from dict into class
        :param data: dict of a type of data
        :param ui: bool, where the data came from
        :return: None
        """
        if not ui and data["command"] == "M145":
            try:
                if int(data["params"]["S"]) == 0:
                    data_class = self.material1
                elif int(data["params"]["S"]) == 1:
                    data_class = self.material2
                else:
                    # unable to parse again - lazy way of not writing duplicate code
                    raise KeyError
            except KeyError:
                # Unable to parse M145
                # noinspection PyProtectedMember
                self.plugin._logger.error("Unable to parse M145 command")
                return
        else:
            data_class = getattr(self, data["name"])

        data_class.params_from_dict(data["params"])

    def to_dict(self):
        # Wraps all the data up to send it to the UI
        result = {}
        for key, data in ALL_DATA_STRUCTURE.items():
            params = getattr(self, key).params_to_dict()
            result[key] = {"command": data["command"], "params": params}

        return result

    def to_list(self):
        result = []
        for key, data in ALL_DATA_STRUCTURE.items():
            params = getattr(self, key).params_to_dict()
            result.append({"name": key, "command": data["command"], "params": params})

        return result
