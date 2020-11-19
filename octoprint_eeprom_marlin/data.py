# -*- coding: utf-8 -*-


COMMAND_PARAMS = {
    "M92": ["X", "Y", "Z", "E"],
    "M203": ["X", "Y", "Z", "E"],
    "M201": ["X", "Y", "Z", "E"],
    "M204": ["P", "R", "T"],
    "M851": ["X", "Y", "Z"],
    "M206": ["X", "Y", "Z"],
    "M666": ["X", "Y", "Z"],
    "M665": ["L", "R", "S", "A", "B", "C"],
    "M900": ["K", "R"],
    "M200": ["D"],
    "M301": ["P", "I", "D"],
    "M304": ["P", "I", "D"],
    "M205": ["S", "T", "B", "X", "Y", "Z", "E"],
    "M420": ["S", "Z"],
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


class IndividualData:
    """
    Holding individual data entries
    """

    name = ""  # type: str
    command = ""  # type: str
    params = {}  # type: dict

    def __init__(self, name, command, params):
        self.name = name
        self.command = command
        for param in params:
            self.params[param] = None

    def params_from_dict(self, data):
        for key, value in data.items():
            self.params[key] = value


class EEPROMData:
    """
    Holds recieved EEPROM data
    """

    def __init__(self):
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
        self.delta = IndividualData("delta", "M665", ["L", "R", "S", "A", "B", "C"])
        self.linear = IndividualData("linear", "M900", ["K", "R"])
        self.filament = IndividualData("filament", "M200", ["D"])
        self.hotend_pid = IndividualData("hotend_pid", "M301", ["P", "I", "D"])
        self.bed_pid = IndividualData("bed_pid", "M304", ["P", "I", "D"])
        self.advanced = IndividualData(
            "advanced", "M205", ["S", "T", "B", "X", "Y", "Z", "E"]
        )
        self.autolevel = IndividualData("autolevel", "M420", ["S", "Z"])

    def data_from_list(self, data):
        """
        Parse data from list into class
        :param data: list of dictionaries to parse
        :return: None
        """
        for item in data:
            data_class = getattr(self, item["name"])
            data_class.params_from_dict(item["params"])

    def data_from_dict(self, data):
        """
        Parse data from dict into class
        :param data: dict of a type of data
        :return: None
        """
        data_class = getattr(self, data["name"])
        data_class.params_from_dict(data["params"])


class ChangedData:
    """
    Tracks changed data, to send to the printer
    TODO This might be better off client side.
    """

    eeprom = None  # type: EEPROMData
    _is_changed = False  # type: bool
    changed_entries = []  # type: list
    # Dict of the IndividualData that need to be saved.

    def is_any_changed(self):
        return self._is_changed

    def add_changed(self, data_class):
        self._is_changed = True
        self.changed_entries.append(data_class)

    def saved(self):
        self._is_changed = False
        self.changed_entries = []
