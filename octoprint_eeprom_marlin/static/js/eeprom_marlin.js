/**
 * Plugin was Created by Salandora on 27.07.2015, Modified by Anderson Silva on 20.08.2017, Contribution of CyberDracula on 15.08.2017.
 * Full maintenance of plugin since 09.2020 (September) by Charlie Powell
 * This file no longer contains any work of previous contributors as of version 3.0
 */

$(function () {
    function EEPROMMarlinViewModel(parameters) {
        var self = this;

        self.printerState = parameters[0];
        self.settingsViewModel = parameters[1];

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

            eeprom.material1 = (function () {
                var material1 = {};

                material1.B = ko.observable();
                material1.F = ko.observable();
                material1.H = ko.observable();
                material1.S = ko.observable();

                material1.visible = ko.computed(function () {
                    for (let param in material1) {
                        if (param === "visible") {
                            continue;
                        }
                        if (material1[param]() !== null) {
                            return true;
                        }
                    }
                    return false;
                });

                return material1;
            })();

            eeprom.material2 = (function () {
                var material2 = {};

                material2.B = ko.observable();
                material2.F = ko.observable();
                material2.H = ko.observable();
                material2.S = ko.observable();

                material2.visible = ko.computed(function () {
                    for (let param in material2) {
                        if (param === "visible") {
                            continue;
                        }
                        if (material2[param]() !== null) {
                            return true;
                        }
                    }
                    return false;
                });

                return material2;
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

            eeprom.filament_change = (function () {
                var filament_change = {};

                filament_change.L = ko.observable();
                filament_change.U = ko.observable();

                filament_change.visible = ko.computed(function () {
                    for (let param in filament_change) {
                        if (param === "visible") {
                            continue;
                        }
                        if (filament_change[param]() !== null) {
                            return true;
                        }
                    }
                    return false;
                });
                return filament_change;
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
            bed_pid: [
                {
                    label: "Bed kP",
                    value: self.eeprom.bed_pid.P,
                    units: null,
                },
                {
                    label: "Bed kI",
                    value: self.eeprom.bed_pid.I,
                    units: null,
                },
                {
                    label: "Bed kD",
                    value: self.eeprom.bed_pid.D,
                    units: null,
                },
            ],
            delta: [
                {
                    label: "Calibration radius",
                    value: self.eeprom.delta.B,
                    units: null,
                },
                {
                    label: "Delta height",
                    value: self.eeprom.delta.H,
                    units: null,
                },
                {
                    label: "Diagonal rod",
                    value: self.eeprom.delta.L,
                    units: null,
                },
                {
                    label: "Segments per second",
                    value: self.eeprom.delta.S,
                    units: null,
                },
                {
                    label: "Alpha (Tower 1) angle trim",
                    value: self.eeprom.delta.X,
                    units: null,
                },
                {
                    label: "Beta (Tower 2) angle trim",
                    value: self.eeprom.delta.Y,
                    units: null,
                },
                {
                    label: "Gamma (Tower 3) angle trim",
                    value: self.eeprom.delta.Z,
                    units: null,
                },
            ],
            endstop: [
                {
                    label: "Adjustment for X",
                    value: self.eeprom.endstop.X,
                    units: "mm",
                },
                {
                    label: "Adjustment for Y",
                    value: self.eeprom.endstop.Y,
                    units: "mm",
                },
                {
                    label: "Adjustment for Z",
                    value: self.eeprom.endstop.Z,
                    units: "mm",
                },
            ],
            feedrate: [
                {
                    label: "X axis",
                    value: self.eeprom.feedrate.X,
                    units: "mm/s",
                },
                {
                    label: "Y axis",
                    value: self.eeprom.feedrate.Y,
                    units: "mm/s",
                },
                {
                    label: "Z axis",
                    value: self.eeprom.feedrate.Z,
                    units: "mm/s",
                },
                {
                    label: "E axis",
                    value: self.eeprom.feedrate.E,
                    units: "mm/s",
                },
            ],
            filament: [
                {
                    label: "Filament Diameter",
                    value: self.eeprom.filament.D,
                    units: "mm",
                },
            ],
            home_offset: [
                {
                    label: "X home offset",
                    value: self.eeprom.home_offset.X,
                    units: "mm",
                },
                {
                    label: "Y home offset",
                    value: self.eeprom.home_offset.Y,
                    units: "mm",
                },
                {
                    label: "Z home offset",
                    value: self.eeprom.home_offset.Z,
                    units: "mm",
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
            linear: [
                {
                    label: "K factor",
                    value: self.eeprom.linear.K,
                    units: null,
                },
            ],
            material1: [
                {
                    label: "Hotend Temperature",
                    value: self.eeprom.material1.H,
                    units: "°C",
                },
                {
                    label: "Bed Temperature",
                    value: self.eeprom.material1.B,
                    units: "°C",
                },
                {
                    label: "Fan Speed",
                    value: self.eeprom.material1.F,
                    units: "0-255",
                },
            ],
            material2: [
                {
                    label: "Hotend Temperature",
                    value: self.eeprom.material2.H,
                    units: "°C",
                },
                {
                    label: "Bed Temperature",
                    value: self.eeprom.material2.B,
                    units: "°C",
                },
                {
                    label: "Fan Speed",
                    value: self.eeprom.material2.F,
                    units: "0-255",
                },
            ],
            max_acceleration: [
                {
                    label: "X maximum acceleration",
                    value: self.eeprom.max_acceleration.X,
                    units: "mm/s2",
                },
                {
                    label: "Y maximum acceleration",
                    value: self.eeprom.max_acceleration.Y,
                    units: "mm/s2",
                },
                {
                    label: "Z maximum acceleration",
                    value: self.eeprom.max_acceleration.Z,
                    units: "mm/s2",
                },
                {
                    label: "E maximum acceleration",
                    value: self.eeprom.max_acceleration.E,
                    units: "mm/s2",
                },
            ],
            print_acceleration: [
                {
                    label: "Printing acceleration",
                    value: self.eeprom.print_acceleration.P,
                    units: "mm/s2",
                },
                {
                    label: "Retract acceleration",
                    value: self.eeprom.print_acceleration.R,
                    units: "mm/s2",
                },
                {
                    label: "Travel acceleration",
                    value: self.eeprom.print_acceleration.T,
                    units: "mm/s2",
                },
            ],
            probe_offset: [
                {
                    label: "Z probe X offset",
                    value: self.eeprom.probe_offset.X,
                    units: "mm",
                },
                {
                    label: "Z probe Y offset",
                    value: self.eeprom.probe_offset.Y,
                    units: "mm",
                },
                {
                    label: "Z probe Z offset",
                    value: self.eeprom.probe_offset.Z,
                    units: "mm",
                },
            ],
            steps: [
                {
                    label: "X steps",
                    value: self.eeprom.steps.X,
                    units: "steps/mm",
                },
                {
                    label: "Y steps",
                    value: self.eeprom.steps.Y,
                    units: "steps/mm",
                },
                {
                    label: "Z steps",
                    value: self.eeprom.steps.Z,
                    units: "steps/mm",
                },
                {
                    label: "E steps",
                    value: self.eeprom.steps.E,
                    units: "steps/mm",
                },
            ],
            filament_change: [
                {
                    label: "Load length",
                    value: self.eeprom.filament_change.L,
                    units: "mm",
                },
                {
                    label: "Unload length",
                    value: self.eeprom.filament_change.U,
                    units: "mm",
                },
            ],
        };

        self.eeprom_from_json = function (data) {
            // loops through response and assigns values to observables
            for (let key in data.eeprom) {
                let value = data.eeprom[key];
                for (let param in value.params) {
                    try {
                        self.eeprom[key][param](value.params[param]);
                    } catch {
                        console.log(key);
                        console.log(param);
                    }
                }
            }
            self.unsaved(false);
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

        self.info_from_json = function (data) {
            self.info.additional([]);
            for (let additional in data.info.additional) {
                if (additional === "FIRMWARE_NAME") {
                    continue;
                }
                let value = data.info.additional[additional];
                let name = capitaliseWords(additional.replace(/_/gi, " "));
                // format report to more human-readable style
                self.info.additional.push({
                    name: name,
                    val: value,
                });
            }
            self.info.capabilities([]);
            for (let capability in data.info.capabilities) {
                let value = data.info.capabilities[capability];
                let cap = capitaliseWords(capability.replace(/_/gi, " "));
                // format cap to more human-readable style
                self.info.capabilities.push({
                    cap: cap,
                    val: value,
                });
            }
            self.info.is_marlin(data.info.is_marlin);
            self.info.name(data.info.name);
        };

        self.backups = ko.observableArray([]);
        self.backup_upload_name = ko.observable();
        self.backup_upload_data = undefined;

        // State bindings
        self.loading = ko.observable(false);
        self.initialLoad = ko.observable(true);
        self.saving = ko.observable(false);
        self.unsaved = ko.observable(false);
        self.enable_fields = ko.pureComputed(function () {
            return (
                !self.loading() &&
                !self.saving() &&
                !self.printerState.isBusy() &&
                self.printerState.isReady()
            );
        });
        self.enable_buttons = ko.pureComputed(function () {
            return (
                !self.loading() &&
                !self.initialLoad() &&
                self.info.is_marlin() &&
                !self.printerState.isBusy() &&
                self.printerState.isReady()
            );
        });

        self.edited = function () {
            if (!self.initialLoad() && !self.loading()) {
                self.unsaved(true);
            }
        };

        self.backup_open = ko.observable(false);

        // Button bindings
        self.load_eeprom = function () {
            self.loading(true);
            OctoPrint.simpleApiCommand("eeprom_marlin", "load");
        };

        self.save_eeprom = function () {
            self.saving(true);
            OctoPrint.simpleApiCommand("eeprom_marlin", "save", {
                eeprom_data: self.eeprom_to_json(),
            }).done(function (response) {
                self.saving(false);
                self.unsaved(false);
            });
        };

        self.reset_eeprom = function () {
            showConfirmationDialog(
                "This will reset the EEPROM settings to factory defaults",
                function () {
                    OctoPrint.simpleApiCommand("eeprom_marlin", "reset");
                },
                {
                    proceed: "Reset",
                }
            );
        };

        self.toggle_backup = function () {
            if ($("#eeprom_tab_backup").hasClass("in")) {
                // backup open, close it
                $("#eeprom_tab_data").collapse("show");
                $("#eeprom_tab_backup").collapse("hide");
                self.backup_open(false);
            } else {
                // backup closed, open it
                $("#eeprom_tab_data").collapse("hide");
                $("#eeprom_tab_backup").collapse("show");
                self.backup_open(true);
            }
        };

        self.backups_from_response = function (data) {
            self.backups(data);
        };

        self.delete_backup = function (name) {
            OctoPrint.simpleApiCommand("eeprom_marlin", "delete", {
                name: name,
            }).done(function (response) {
                let success = response.success;
                if (!success) {
                    new PNotify({
                        title: "Error creating a backup",
                        text: response.error,
                        type: "error",
                        hide: false,
                    });
                } else {
                    self.backups_from_response(response.backups);
                }
            });
        };

        self.backup_name = ko.observable();

        self.new_backup = function () {
            console.log(
                self.settingsViewModel.settings.plugins.eeprom_marlin.custom_name()
            );
            if (
                self.settingsViewModel.settings.plugins.eeprom_marlin.custom_name()
            ) {
                // Trigger modal with custom name
                $("#eepromBackupNameModal").modal("show");
            } else {
                self.create_backup();
            }
        };

        self.create_backup = function () {
            $("#eepromBackupNameModal").modal("hide");

            var payload = {};
            if (
                self.settingsViewModel.settings.plugins.eeprom_marlin.custom_name()
            ) {
                payload = { name: self.backup_name() };
            }
            self.backup_name("");

            OctoPrint.simpleApiCommand("eeprom_marlin", "backup", payload).done(
                function (response) {
                    let success = response.success;
                    if (!success) {
                        new PNotify({
                            title: "Error creating a backup",
                            text: response.error,
                            type: "error",
                            hide: false,
                        });
                    } else {
                        new PNotify({
                            title: "Backup created successfully",
                            type: "success",
                            hide: true,
                            delay: 4000,
                        });
                        OctoPrint.simpleApiGet("eeprom_marlin").done(function (
                            response
                        ) {
                            self.backups_from_response(response.backups);
                        });
                    }
                }
            );
        };

        self.restore_backup = function (name) {
            OctoPrint.simpleApiCommand("eeprom_marlin", "restore", {
                name: name,
            }).done(function (response) {
                let success = response.success;
                if (!success) {
                    new PNotify({
                        title: "Error restoring backup",
                        text: response.error,
                        type: "error",
                        hide: false,
                    });
                } else {
                    new PNotify({
                        title: "Backup restored successfully",
                        text: "Restored " + response.name,
                        type: "success",
                        hide: true,
                        delay: 4000,
                    });
                    self.eeprom_from_json(response.eeprom);
                }
            });
        };

        $("#plugin_eeprom_marlin_backup_upload").fileupload({
            dataType: "json",
            maxNumberOfFiles: 1,
            autoUpload: false,
            headers: OctoPrint.getRequestHeaders(),
            add: function (e, data) {
                if (data.files.length === 0) {
                    // no files? ignore
                    return false;
                }

                self.backup_upload_name(data.files[0].name);
                self.backup_upload_data = data;
            },
            done: function (e, data) {
                self.backup_upload_name(undefined);
                self.backup_upload_name = undefined;
            },
        });

        self.restore_from_upload = function () {
            if (self.backup_upload_data === undefined) return;
            var input, file, fr;

            if (typeof window.FileReader !== "function") {
                alert("The file API is not supported on this browser");
                return;
            }

            file = self.backup_upload_data.files[0];
            fr = new FileReader();
            fr.onload = recievedText;
            fr.readAsText(file);

            function recievedText(e) {
                let lines = e.target.result;
                var json_data = JSON.parse(lines);
                OctoPrint.simpleApiCommand("eeprom_marlin", "upload_restore", {
                    data: json_data,
                }).done(function (response) {
                    let success = response.success;
                    if (!success) {
                        new PNotify({
                            title: "Error restoring backup",
                            text: response.error,
                            type: "error",
                            hide: false,
                        });
                    } else {
                        new PNotify({
                            title: "Backup restored successfully",
                            type: "success",
                            hide: true,
                            delay: 4000,
                        });
                        self.eeprom_from_json(response.eeprom);
                    }
                    $("#eepromUploadBackupModal").modal("hide");
                });
            }
        };

        // DataUpdater
        self.onDataUpdaterPluginMessage = function (plugin, data) {
            if (plugin !== "eeprom_marlin") {
                return;
            }
            if (data.type === "load") {
                console.log(data);
                self.eeprom_from_json(data.data);
                self.info_from_json(data.data);
                self.loading(false);
            }
        };

        self.onAllBound = self.onEventConnected = function () {
            self.loading(true);
            OctoPrint.simpleApiGet("eeprom_marlin").done(function (response) {
                self.eeprom_from_json(response);
                self.info_from_json(response);
                self.backups_from_response(response.backups);
                self.loading(false);
                self.initialLoad(false);
            });
        };

        // Utilities
        function capitaliseWords(str) {
            return str.replace(/\w\S*/g, function (txt) {
                return (
                    txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase()
                );
            });
        }
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: EEPROMMarlinViewModel,
        dependencies: ["printerStateViewModel", "settingsViewModel"],
        elements: ["#tab_plugin_eeprom_marlin"],
    });
});
