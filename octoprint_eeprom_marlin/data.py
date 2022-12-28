from __future__ import annotations

__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = (
    "Copyright (C) 2020 Charlie Powell - Released under terms of the AGPLv3 License"
)

import copy
from dataclasses import asdict, dataclass, field

from octoprint.util import dict_merge

# This defines the data structure used in both the frontend and the backend. Must be kept in sync with
# the observables in the viewmodel. UI will update automatically from this structure using the Jinja templates.
# JAVASCRIPT OBSERVABLES MUST ALSO BE UPDATED
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
        "switches": ["T"],
        "name": "Steps",
        "link": "https://marlinfw.org/docs/gcode/M092.html",
    },
    "feedrate": {
        "command": "M203",
        "params": {
            "X": {"type": "float1", "label": "X axis", "units": "mm/s"},
            "Y": {"type": "float1", "label": "Y axis", "units": "mm/s"},
            "Z": {"type": "float1", "label": "Z axis", "units": "mm/s"},
            "E": {"type": "float1", "label": "E axis", "units": "mm/s"},
        },
        "switches": ["T"],
        "name": "Feedrate",
        "link": "https://marlinfw.org/docs/gcode/M203.html",
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
        "switches": ["T"],
        "name": "Maximum Acceleration",
        "link": "https://marlinfw.org/docs/gcode/M201.html",
    },
    "print_acceleration": {
        "command": "M204",
        "params": {
            "P": {"type": "float1", "label": "Printing acceleration", "units": "mm/s2"},
            "R": {"type": "float1", "label": "Retract acceleration", "units": "mm/s2"},
            "T": {"type": "float1", "label": "Travel acceleration", "units": "mm/s2"},
        },
        "name": "Print Acceleration",
        "link": "https://marlinfw.org/docs/gcode/M204.html",
    },
    "probe_offset": {
        "command": "M851",
        "params": {
            "X": {"type": "float2", "label": "Z probe X offset", "units": "mm"},
            "Y": {"type": "float2", "label": "Z probe Y offset", "units": "mm"},
            "Z": {"type": "float2", "label": "Z probe Z offset", "units": "mm"},
        },
        "name": "Probe Offset",
        "link": "https://marlinfw.org/docs/gcode/M851.html",
    },
    "home_offset": {
        "command": "M206",
        "params": {
            "X": {"type": "float2", "label": "X home offset", "units": "mm"},
            "Y": {"type": "float2", "label": "Y home offset", "units": "mm"},
            "Z": {"type": "float2", "label": "Z home offset", "units": "mm"},
        },
        "name": "Home Offset",
        "link": "https://marlinfw.org/docs/gcode/M206.html",
    },
    "endstop": {
        "command": "M666",
        "params": {
            "X": {"type": "float2", "label": "Adjustment for X", "units": "mm"},
            "Y": {"type": "float2", "label": "Adjustment for Y", "units": "mm"},
            "Z": {"type": "float2", "label": "Adjustment for Z", "units": "mm"},
        },
        "name": "Endstop Offsets",
        "link": "https://marlinfw.org/docs/gcode/M666.html",
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
        "link": "https://marlinfw.org/docs/gcode/M665.html",
    },
    "linear": {
        "command": "M900",
        "params": {"K": {"type": "float2", "label": "K factor"}},
        "switches": ["T"],
        "name": "Linear Advance",
        "link": "https://marlinfw.org/docs/gcode/M900.html",
    },
    "filament": {
        "command": "M200",
        "params": {
            "D": {"type": "float2", "label": "Filament Diameter", "units": "mm"}
        },
        "switches": ["T"],
        "name": "Filament Settings",
        "link": "https://marlinfw.org/docs/gcode/M200.html",
    },
    "hotend_pid": {
        "command": "M301",
        "params": {
            "P": {"type": "float2", "label": "Hotend kP"},
            "I": {"type": "float2", "label": "Hotend kI"},
            "D": {"type": "float2", "label": "Hotend kD"},
        },
        "switches": ["E"],
        "name": "Hotend PID",
        "link": "https://marlinfw.org/docs/gcode/M301.html",
    },
    "bed_pid": {
        "command": "M304",
        "params": {
            "P": {"type": "float2", "label": "Bed kP"},
            "I": {"type": "float2", "label": "Bed kI"},
            "D": {"type": "float2", "label": "Bed kD"},
        },
        "name": "Bed PID",
        "link": "https://marlinfw.org/docs/gcode/M304.html",
    },
    "hotend_mpc": {
        "command": "M306",
        "params": {
            "A": {
                "type": "float2",
                "label": "Ambient heat transfer coefficient (no fan)",
            },
            "C": {"type": "float2", "label": "Heatblock capacity", "untits": "J/K"},
            "F": {
                "type": "float2",
                "label": "Ambient heat transfer coefficient (fan on full).",
            },
            "H": {
                "type": "float2",
                "label": "Filament heat capacity",
                "units": "J/K/mm",
            },
            "P": {"type": "int", "label": "Heater power", "units": "W"},
            "R": {"type": "int", "label": "Sensor responsiveness"},
        },
        "switches": ["E"],
        "name": "Hotend MPC",
        "link": "https://marlinfw.org/docs/gcode/M306.html",
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
        "link": "https://marlinfw.org/docs/gcode/M205.html",
    },
    "autolevel": {
        "command": "M420",
        "params": {
            "S": {"type": "bool", "label": "Enabled"},
            "Z": {"type": "float1", "label": "Z fade height", "units": "mm"},
        },
        "name": "Autolevel",
        "link": "https://marlinfw.org/docs/gcode/M420.html",
    },
    "material": {
        "command": "M145",
        "params": {
            "H": {"type": "float1", "label": "Hotend temperature", "units": "°C"},
            "B": {"type": "float1", "label": "Bed temperature", "units": "°C"},
            "F": {"type": "int", "label": "Fan speed", "units": "0-255"},
        },
        "switches": ["S"],
    },
    "filament_change": {
        "command": "M603",
        "params": {
            "L": {"type": "float1", "label": "Load length", "units": "mm"},
            "U": {"type": "float1", "label": "Unload length", "units": "mm"},
        },
        "name": "Filament Change",
        "link": "https://marlinfw.org/docs/gcode/M603.html",
    },
    "filament_runout": {
        "command": "M412",
        "params": {
            "D": {"type": "float2", "label": "Runout Distance", "units": "mm"},
            "H": {"type": "bool", "label": "Enable host handling of filament runout"},
            "S": {"type": "bool", "label": "Enable filament runout sensor"},
        },
        "name": "Filament Runout Sensor",
        "link": "https://marlinfw.org/docs/gcode/M412.html",
    },
    "tmc_current": {
        "command": "M906",
        "params": {
            "E": {"type": "float2", "label": "Current for E0 Stepper", "units": "mA"},
            "X": {"type": "float2", "label": "Current for X Stepper", "units": "mA"},
            "Y": {"type": "float2", "label": "Current for Y Stepper", "units": "mA"},
            "Z": {"type": "float2", "label": "Current for Z Stepper", "units": "mA"},
        },
        "switches": ["I", "T"],
        "link": "https://marlinfw.org/docs/gcode/M906.html",
    },
    "tmc_hybrid": {
        "command": "M913",
        "params": {
            "X": {"type": "float2", "label": "Hybrid Threshold for X axis"},
            "Y": {"type": "float2", "label": "Hybrid Threshold for Y axis"},
            "Z": {"type": "float2", "label": "Hybrid Threshold for Z axis"},
            "E": {"type": "float2", "label": "Hybrid Threshold for E axis"},
        },
        "link": "https://marlinfw.org/docs/gcode/M913.html",
        "switches": ["I", "T"],
    },
    "input_shaping": {
        "command": "M593",
        "params": {
            "F": {"type": "float2", "label": "Damping Frequency", "units": "hz"},
            "D": {"type": "float2", "label": "Zeta/damping factor"},
        },
        "link": "https://marlinfw.org/docs/gcode/M593.html",
        "name": "Input Shaping (both axes)",
    },
}


def find_name_from_command(command):
    for key, data in ALL_DATA_STRUCTURE.items():
        if command == data["command"]:
            return key
    else:
        raise ValueError


@dataclass
class FirmwareInfo:
    """
    Holds firmware info data
    """

    name: str = ""
    is_marlin: bool = False
    additional: dict = field(default_factory=dict)
    capabilities: dict = field(default_factory=dict)
    locked: bool = False

    def additional_info_from_dict(self, data):
        self.additional = {}
        for key, value in data.items():
            self.additional[key] = value

    def add_capabilities(self, caps):
        for capability, value in caps.items():
            self.capabilities[capability] = value

    def to_dict(self):
        # For sending to UI
        return asdict(self)


@dataclass
class IndividualData:
    """
    Holding individual data entries
    """

    name: str = ""
    command: str = ""
    params: dict = field(default_factory=dict)

    def __post_init__(self):
        for param in self.params:
            self.params[param]["value"] = None

    def params_from_dict(self, data):
        for key, value in data.items():
            if value is not None:
                if key not in self.params:
                    self.params[key] = {}
                self.params[key]["value"] = value

    def params_to_dict(self):
        # Ready to send to the UI
        params = {}
        for param, data in self.params.items():
            try:
                params[param] = data["value"]
            except Exception:
                # This is hit in the case of materials, where the S value is not stored
                # Safely ignored (not pretty I know)
                continue

        return params

    def generate_command(self):
        command = self.command
        for param, data in self.params.items():
            if data["value"] is None:
                continue
            command += " " + param + data["value"]

        return command


class MultipleData:
    """
    Eg. for the TMC drivers 'Hybrid Threshold'
    echo:; Hybrid Threshold:
    echo:  M913 X229 Y229 Z164
    echo:  M913 I1 Z164
    echo:  M913 T0 E19
    {
    "I1": { IndividualData },
    "T0": { IndividualData },
    }
    """

    # def __post_init__(self):
    #     self.data = {}
    #     for switch in self.switches:
    #         self.data[switch] = IndividualData()

    def __init__(self, name, command, switches):
        self.name = name
        self.command = command
        self.switches = switches
        self.data = {}
        for param, content in ALL_DATA_STRUCTURE[name]["params"].items():
            self.data[param] = content
            self.data[param]["value"] = None

    def data_for_switch(self, switch):
        if switch in self.switches:
            return self.data[switch]

    def set_data_for_switch(self, switch, data):
        if switch[0] not in self.switches:
            raise ValueError("unknown switch")

        if switch not in data:
            # This particular switch not seen, so create data class for it
            self.data[switch] = IndividualData(
                name=self.name,
                command=self.command,
                params=copy.deepcopy(ALL_DATA_STRUCTURE[self.name]["params"]),
            )

        self.data[switch].params_from_dict(data)

    def set_data_no_switch(self, data):
        if not data:
            return
        for key, value in data.items():
            if value is not None:
                if key not in self.data:
                    self.data[key] = {}
                self.data[key]["value"] = value

    def is_switch_valid(self, switch):
        return switch[0] in self.switches

    def params_to_dict(self):
        params = {}
        for key, value in self.data.items():
            if key[0] in self.switches:
                params[key] = value.params_to_dict()
            else:
                params[key] = value["value"]

        return params


class EEPROMData:
    """
    Holds recieved EEPROM data
    """

    def __init__(self, plugin):
        self.plugin = plugin

        for key, data in ALL_DATA_STRUCTURE.items():
            data = copy.deepcopy(data)  # Avoid modifying the constant
            if "switches" in data:
                # Supports multiple sets of data
                # Switched on one parameter
                setattr(
                    self,
                    key,
                    MultipleData(
                        key,
                        data["command"],
                        data["switches"],
                    ),
                )
            else:
                setattr(self, key, IndividualData(key, data["command"], data["params"]))

        # noinspection PyProtectedMember
        self.plugin._logger.info("EEPROM Data initialised")

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

        try:
            data_class = getattr(self, data["name"])
        except AttributeError:
            # noinspection PyProtectedMember
            self.plugin._logger.error(
                "Could not parse data, name was {}".format(data["name"])
            )
            return

        if type(data_class) == MultipleData:
            for param, value in data["params"].items():
                if type(value) == dict:
                    data_class.set_data_for_switch(param, value)
                else:
                    data_class.set_data_no_switch({param: value})

        else:
            data_class.params_from_dict(data["params"])

    def from_parser(self, data):
        try:
            data_class = getattr(self, data["name"])
        except AttributeError:
            # noinspection PyProtectedMember
            self.plugin._logger.error(
                "Could not parse data, name was {}".format(data["name"])
            )
            return

        if type(data_class) == MultipleData:
            # Work out which parameter is the switch
            params = data["params"].keys()
            switches = list({p[0] for p in params}.intersection(data_class.switches))
            if len(switches) == 0:
                # No switches
                data_class.set_data_no_switch(data["params"])
            else:
                # We ignore the fact there could be more than one switch and use
                # only the first
                switch_value = data["params"][switches[0]]
                # Remove switch from params, so it's not set on data
                data["params"].pop(switches[0])
                data_class.set_data_for_switch(
                    f"{switches[0]}{switch_value}", data["params"]
                )
        else:
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


class FirmwareStats:
    def __init__(self):
        self.stats = copy.deepcopy(blank_stats)

    def update_stats(self, new_stats):
        self.stats = dict_merge(self.stats, new_stats)

    def get_stats(self):
        return self.stats


blank_stats = {
    "prints": 0,
    "finished": 0,
    "failed": 0,
    "total_time": "",
    "longest": "",
    "filament": "",
}
