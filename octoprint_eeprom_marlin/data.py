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

COMMAND_PARAMS = {
    "M92": ["X", "Y", "Z", "E"],
    "M203": ["X", "Y", "Z", "E"],
    "M201": ["X", "Y", "Z", "E"],
    "M204": ["P", "R", "T"],
    "M851": ["X", "Y", "Z"],
    "M206": ["X", "Y", "Z"],
    "M666": ["X", "Y", "Z"],
    "M665": ["L", "R", "H", "S", "X", "Y", "Z", "A", "B", "C"],
    "M900": ["K"],
    "M200": ["D"],
    "M301": ["P", "I", "D"],
    "M304": ["P", "I", "D"],
    "M205": ["S", "T", "B", "X", "Y", "Z", "E", "J"],
    "M420": ["S", "Z"],
    "M145": ["S", "B", "H", "F"],
    "M603": ["L", "U"],
}

COMMAND_NAMES = {
    "M92": "steps",
    "M203": "feedrate",
    "M201": "max_acceleration",
    "M204": "print_acceleration",
    "M851": "probe_offset",
    "M206": "home_offset",
    "M666": "endstop",
    "M665": "delta",
    "M900": "linear",
    "M200": "filament",
    "M301": "hotend_pid",
    "M304": "bed_pid",
    "M205": "advanced",
    "M420": "autolevel",
    "M145": "material",
    "M603": "filament_change",
}


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
        self.params = {}  # type: Dict[str, Optional[float]]
        for param in params:
            self.params[param] = None

    def params_from_dict(self, data):
        for key, value in data.items():
            if value is not None:
                self.params[key] = float(value)


class EEPROMData:
    """
    Holds recieved EEPROM data
    """

    def __init__(self, plugin):
        self.plugin = plugin

        self.steps = IndividualData("steps", "M92", ["X", "Y", "Z", "E"])
        self.feedrate = IndividualData("feedrate", "M203", ["X", "Y", "Z", "E"])
        self.max_acceleration = IndividualData(
            "max_acceleration", "M201", ["X", "Y", "Z", "E"]
        )
        self.print_acceleration = IndividualData(
            "print_acceleration", "M204", ["P", "R", "T"]
        )
        self.probe_offset = IndividualData("probe_offset", "M851", ["X", "Y", "Z"])
        self.home_offset = IndividualData("home_offset", "M206", ["X", "Y", "Z"])
        self.endstop = IndividualData("endstop", "M666", ["X", "Y", "Z"])
        self.delta = IndividualData(
            "delta", "M665", ["L", "R", "H", "S", "X", "Y", "Z", "A", "B", "C"]
        )
        self.linear = IndividualData("linear", "M900", ["K"])
        self.filament = IndividualData("filament", "M200", ["D"])
        self.hotend_pid = IndividualData("hotend_pid", "M301", ["P", "I", "D"])
        self.bed_pid = IndividualData("bed_pid", "M304", ["P", "I", "D"])
        self.advanced = IndividualData(
            "advanced", "M205", ["S", "T", "B", "X", "Y", "Z", "E", "J"]
        )
        self.autolevel = IndividualData("autolevel", "M420", ["S", "Z"])
        self.material1 = IndividualData("material1", "M145", ["S", "B", "H", "F"])
        self.material2 = IndividualData("material2", "M145", ["S", "B", "H", "F"])
        self.filament_change = IndividualData(
            "filament_change", "M603", COMMAND_PARAMS["M603"]
        )

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
        if not ui and data["command"] == "M145":
            try:
                if int(data["params"]["S"]) == 0:
                    data_class = self.material1
                elif int(data["params"]["S"]) == 1:
                    data_class = self.material2
                else:
                    # unable to parse again
                    # noinspection PyProtectedMember
                    self.plugin._logger.error("Unable to parse M145 command")
                    return
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
        data = {}
        for command, name in COMMAND_NAMES.items():
            if command == "M145":
                # Special handling for M145 data
                cls = getattr(self, name + "1")
                data[name + "1"] = {"command": command, "params": cls.params}
                cls2 = getattr(self, name + "2")
                data[name + "2"] = {"command": command, "params": cls2.params}
            else:
                cls = getattr(self, name)
                data[name] = {"command": command, "params": cls.params}

        return data

    def to_list(self):
        data = []
        for command, name in COMMAND_NAMES.items():
            if command == "M145":
                # Special handling for M145 data
                params = getattr(self, name + "1").params
                data.append({"name": name + "1", "command": command, "params": params})
                params2 = getattr(self, name + "2").params
                data.append({"name": name + "2", "command": command, "params": params2})
            else:
                params = getattr(self, name).params
                data.append({"name": name, "command": command, "params": params})
