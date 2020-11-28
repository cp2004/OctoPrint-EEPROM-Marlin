/**
 * Plugin was Created by Salandora on 27.07.2015, Modified by Anderson Silva on 20.08.2017, Contribution of CyberDracula on 15.08.2017.
 * Full maintenance of plugin since 09.2020 (September) by Charlie Powell
 * This file no longer contains any work of previous contributors
 */

$(function () {
    function EEPROMMarlinViewModel(parameters) {
        var self = this;

        self.settingsViewModel = parameters[0];

        self.eeprom = (function () {
            var eeprom = {};

            eeprom.advanced = (function () {
                var advanced = {};

                advanced.B = ko.observable();
                advanced.E = ko.observable();
                advanced.J = ko.observable();
                advanced.S = ko.observable();
                advanced.T = ko.observable();
                advanced.X = ko.observable();
                advanced.Y = ko.observable();
                advanced.Z = ko.observable();

                advanced.visible = ko.computed(function () {
                    for (let param in advanced) {
                        if (param === "visible") {
                            continue;
                        }
                        if (advanced[param]() !== null) {
                            return true;
                        }
                    }
                    return false;
                });

                return advanced;
            })();

            eeprom.autolevel = (function () {
                var autolevel = {};

                autolevel.S = ko.observable();
                autolevel.Z = ko.observable();

                autolevel.visible = ko.computed(function () {
                    for (let param in autolevel) {
                        if (param === "visible") {
                            continue;
                        }
                        if (autolevel[param]() !== null) {
                            return true;
                        }
                    }
                    return false;
                });

                return autolevel;
            })();

            eeprom.bed_pid = (function () {
                var bed_pid = {};

                bed_pid.D = ko.observable();
                bed_pid.I = ko.observable();
                bed_pid.P = ko.observable();

                bed_pid.visible = ko.computed(function () {
                    for (let param in bed_pid) {
                        if (param === "visible") {
                            continue;
                        }
                        if (bed_pid[param]() !== null) {
                            return true;
                        }
                    }
                    return false;
                });

                return bed_pid;
            })();

            eeprom.delta = (function () {
                var delta = {};

                delta.B = ko.observable();
                delta.H = ko.observable();
                delta.L = ko.observable();
                delta.R = ko.observable();
                delta.S = ko.observable();
                delta.X = ko.observable();
                delta.Y = ko.observable();
                delta.Z = ko.observable();

                delta.visible = ko.computed(function () {
                    for (let param in delta) {
                        if (param === "visible") {
                            continue;
                        }
                        if (delta[param]() !== null) {
                            return true;
                        }
                    }
                    return false;
                });

                return delta;
            })();

            eeprom.endstop = (function () {
                var endstop = {};

                endstop.X = ko.observable();
                endstop.Y = ko.observable();
                endstop.Z = ko.observable();

                endstop.visible = ko.computed(function () {
                    for (let param in endstop) {
                        if (param === "visible") {
                            continue;
                        }
                        if (endstop[param]() !== null) {
                            return true;
                        }
                    }
                    return false;
                });

                return endstop;
            })();

            eeprom.feedrate = (function () {
                var feedrate = {};

                feedrate.E = ko.observable();
                feedrate.X = ko.observable();
                feedrate.Y = ko.observable();
                feedrate.Z = ko.observable();

                feedrate.visible = ko.computed(function () {
                    for (let param in feedrate) {
                        if (param === "visible") {
                            continue;
                        }
                        if (feedrate[param]() !== null) {
                            return true;
                        }
                    }
                    return false;
                });

                return feedrate;
            })();

            eeprom.filament = (function () {
                var filament = {};

                filament.D = ko.observable();

                filament.visible = ko.computed(function () {
                    for (let param in filament) {
                        if (param === "visible") {
                            continue;
                        }
                        if (filament[param]() !== null) {
                            return true;
                        }
                    }
                    return false;
                });

                return filament;
            })();

            eeprom.home_offset = (function () {
                var home_offset = {};

                home_offset.X = ko.observable();
                home_offset.Y = ko.observable();
                home_offset.Z = ko.observable();

                home_offset.visible = ko.computed(function () {
                    for (let param in home_offset) {
                        if (param === "visible") {
                            continue;
                        }
                        if (home_offset[param]() !== null) {
                            return true;
                        }
                    }
                    return false;
                });

                return home_offset;
            })();

            eeprom.hotend_pid = (function () {
                var hotend_pid = {};

                hotend_pid.D = ko.observable();
                hotend_pid.I = ko.observable();
                hotend_pid.P = ko.observable();

                hotend_pid.visible = ko.computed(function () {
                    for (let param in hotend_pid) {
                        if (param === "visible") {
                            continue;
                        }
                        if (hotend_pid[param]() !== null) {
                            return true;
                        }
                    }
                    return false;
                });

                return hotend_pid;
            })();

            eeprom.linear = (function () {
                var linear = {};

                linear.K = ko.observable();

                linear.visible = ko.computed(function () {
                    for (let param in linear) {
                        if (param === "visible") {
                            continue;
                        }
                        if (linear[param]() !== null) {
                            return true;
                        }
                    }
                    return false;
                });

                return linear;
            })();

            eeprom.max_acceleration = (function () {
                var max_acceleration = {};

                max_acceleration.E = ko.observable();
                max_acceleration.X = ko.observable();
                max_acceleration.Y = ko.observable();
                max_acceleration.Z = ko.observable();

                max_acceleration.visible = ko.computed(function () {
                    for (let param in max_acceleration) {
                        if (param === "visible") {
                            continue;
                        }
                        if (max_acceleration[param]() !== null) {
                            return true;
                        }
                    }
                    return false;
                });

                return max_acceleration;
            })();

            eeprom.print_acceleration = (function () {
                var print_acceleration = {};

                print_acceleration.P = ko.observable();
                print_acceleration.R = ko.observable();
                print_acceleration.T = ko.observable();

                print_acceleration.visible = ko.computed(function () {
                    for (let param in print_acceleration) {
                        if (param === "visible") {
                            continue;
                        }
                        if (print_acceleration[param]() !== null) {
                            return true;
                        }
                    }
                    return false;
                });

                return print_acceleration;
            })();

            eeprom.probe_offset = (function () {
                var probe_offset = {};

                probe_offset.X = ko.observable();
                probe_offset.Y = ko.observable();
                probe_offset.Z = ko.observable();

                probe_offset.visible = ko.computed(function () {
                    for (let param in probe_offset) {
                        if (param === "visible") {
                            continue;
                        }
                        if (probe_offset[param]() !== null) {
                            return true;
                        }
                    }
                    return false;
                });

                return probe_offset;
            })();

            eeprom.steps = (function () {
                var steps = {};

                steps.X = ko.observable();
                steps.Y = ko.observable();
                steps.Z = ko.observable();
                steps.E = ko.observable();

                steps.visible = ko.computed(function () {
                    for (let param in steps) {
                        if (param === "visible") {
                            continue;
                        }
                        if (steps[param]() !== null) {
                            return true;
                        }
                    }
                    return false;
                });

                return steps;
            })();

            return eeprom;
        })();

        /* Construct the UI here, in text form to save on markup
         * parameters (all are required):
         * label: Concise & descriptive
         * value: observable
         * units: if applicable, otherwise null
         */
        self.UI = {
            advanced: [
                {
                    label: "Minimum segment time",
                    value: self.eeprom.advanced.B,
                    units: "µs",
                },
                {
                    label: "E max jerk",
                    value: self.eeprom.advanced.E,
                    units: "mm/s",
                },
                {
                    label: "Junction deviation",
                    value: self.eeprom.advanced.J,
                    units: null,
                },
                {
                    label: "Minimum feedrate for print moves",
                    value: self.eeprom.advanced.S,
                    units: "mm/s",
                },
                {
                    label: "Minimum feedrate for travel moves",
                    value: self.eeprom.advanced.T,
                    units: "mms/s",
                },
                {
                    label: "X max jerk",
                    value: self.eeprom.advanced.X,
                    units: "mm/s",
                },
                {
                    label: "Y max jerk",
                    value: self.eeprom.advanced.Y,
                    units: "mm/s",
                },
                {
                    label: "Z max jerk",
                    value: self.eeprom.advanced.Z,
                    units: "mm/s",
                },
            ],
            hotend_pid: [
                {
                    label: "Hotend kP",
                    value: self.eeprom.hotend_pid.P,
                    units: null,
                },
                {
                    label: "Hotend kI",
                    value: self.eeprom.hotend_pid.I,
                    units: null,
                },
                {
                    label: "Hotend kD",
                    value: self.eeprom.hotend_pid.D,
                    units: null,
                },
            ],
            bed_pid: [
                {
                    label: "Bed kP",
                    value: self.eeprom.hotend_pid.P,
                    units: null,
                },
                {
                    label: "Bed kI",
                    value: self.eeprom.hotend_pid.I,
                    units: null,
                },
                {
                    label: "Bed kD",
                    value: self.eeprom.hotend_pid.D,
                    units: null,
                },
            ],
            autolevel: [
                {
                    label: "Enabled",
                    value: self.eeprom.autolevel.S,
                    units: "0/1",
                },
                {
                    label: "Z fade height",
                    value: self.eeprom.autolevel.Z,
                    units: "mm",
                },
            ],
        };

        self.eeprom_from_json = function (data) {
            // loops through response and assigns values to observables
            for (let key in data.eeprom) {
                let value = data.eeprom[key];
                for (let param in value.params) {
                    self.eeprom[key][param](value.params[param]);
                }
            }
        };

        self.eeprom_to_json = function () {
            // loops through eeprom data, to create a JSON object to POST
            var eeprom = [];
            for (let key in self.eeprom) {
                let data = { name: key, params: {} };
                let value = self.eeprom[key];
                for (let param in value) {
                    if (param !== "visible") {
                        data.params[param] = value[param]();
                    }
                }
                eeprom.push(data);
            }
            return eeprom;
        };

        self.info = (function () {
            var info = {};

            info.additional = ko.observableArray([]);
            info.capabilities = ko.observableArray([]);
            info.is_marlin = ko.observable(false);
            info.name = ko.observable();
            return info;
        })();

        function info_from_json(data) {
            self.info.additional(data.info.additional);
            self.info.capabilities(data.info.capabilities);
            self.info.is_marlin(data.info.is_marlin);
            self.info.name(data.info.name);
        }

        // State bindings
        self.loading = ko.observable(false);
        self.saving = ko.observable(false);
        self.controls_enabled = ko.observable(true);

        // Button bindings
        self.load_eeprom = function () {
            self.loading(true);
            OctoPrint.simpleApiCommand("eeprom_marlin", "load");
        };

        self.save_eeprom = function () {
            self.saving(true);
            OctoPrint.simpleApiCommand("eeprom_marlin", "save", {
                eeprom_data: self.eeprom_to_json(),
            });
        };

        // DataUpdater
        self.onDataUpdaterPluginMessage = function (plugin, data) {
            if (plugin !== "eeprom_marlin") {
                return;
            }
            if (data.type === "load") {
                console.log(data);
                self.eeprom_from_json(data.data);
                self.loading(false);
            }
        };

        self.onAllBound = function () {
            OctoPrint.simpleApiGet("eeprom_marlin").done(function (response) {
                self.eeprom_from_json(response);
                info_from_json(response);
                console.log(self.eeprom_to_json());
            });
        };
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: EEPROMMarlinViewModel,
        dependencies: ["settingsViewModel"],
        elements: ["#tab_plugin_eeprom_marlin_2"],
    });
});
