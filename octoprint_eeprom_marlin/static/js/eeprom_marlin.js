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
                advanced.S = ko.observable();
                advanced.T = ko.observable();
                advanced.X = ko.observable();
                advanced.Y = ko.observable();
                advanced.Z = ko.observable();

                return advanced;
            })();

            eeprom.autolevel = (function () {
                var autolevel = {};

                autolevel.S = ko.observable();
                autolevel.Z = ko.observable();

                return autolevel;
            })();

            eeprom.bed_pid = (function () {
                var bed_pid = {};

                bed_pid.D = ko.observable();
                bed_pid.I = ko.observable();
                bed_pid.P = ko.observable();

                return bed_pid;
            })();

            eeprom.delta = (function () {
                var delta = {};

                delta.A = ko.observable();
                delta.B = ko.observable();
                delta.C = ko.observable();
                delta.L = ko.observable();
                delta.R = ko.observable();
                delta.S = ko.observable();

                return delta;
            })();

            eeprom.endstop = (function () {
                var endstop = {};

                endstop.X = ko.observable();
                endstop.Y = ko.observable();
                endstop.Z = ko.observable();

                return endstop;
            })();

            eeprom.feedrate = (function () {
                var feedrate = {};

                feedrate.E = ko.observable();
                feedrate.X = ko.observable();
                feedrate.Y = ko.observable();
                feedrate.Z = ko.observable();

                return feedrate;
            })();

            eeprom.filament = (function () {
                var filament = {};

                filament.D = ko.observable();

                return filament;
            })();

            eeprom.home_offset = (function () {
                var home_offset = {};

                home_offset.X = ko.observable();
                home_offset.Y = ko.observable();
                home_offset.Z = ko.observable();

                return home_offset;
            })();

            eeprom.hotend_pid = (function () {
                var hotend_pid = {};

                hotend_pid.D = ko.observable();
                hotend_pid.I = ko.observable();
                hotend_pid.P = ko.observable();

                return hotend_pid;
            })();

            eeprom.linear = (function () {
                var linear = {};

                linear.K = ko.observable();
                linear.R = ko.observable();

                return linear;
            })();

            eeprom.max_acceleration = (function () {
                var max_acceleration = {};

                max_acceleration.E = ko.observable();
                max_acceleration.X = ko.observable();
                max_acceleration.Y = ko.observable();
                max_acceleration.Z = ko.observable();

                return max_acceleration;
            })();

            eeprom.print_acceleration = (function () {
                var print_acceleration = {};

                print_acceleration.P = ko.observable();
                print_acceleration.R = ko.observable();
                print_acceleration.T = ko.observable();

                return print_acceleration;
            })();

            eeprom.probe_offset = (function () {
                var probe_offset = {};

                probe_offset.X = ko.observable();
                probe_offset.Y = ko.observable();
                probe_offset.Z = ko.observable();

                return probe_offset;
            })();

            eeprom.steps = (function () {
                var steps = {};

                steps.X = ko.observable();
                steps.Y = ko.observable();
                steps.Z = ko.observable();
                steps.E = ko.observable();

                return steps;
            })();

            return eeprom;
        })();

        function eeprom_from_json(data) {
            // loops through response and assigns values to observables
            for (let key in data.eeprom) {
                let value = data.eeprom[key];
                for (let param in value.params) {
                    self.eeprom[key][param](value.params[param]);
                }
            }
        }

        function eeprom_to_json(data) {
            // loops through eeprom data, to create a JSON object to POST
            var eeprom = {};
            for (let key in self.eeprom) {
                let value = self.eeprom[key];
                eeprom[key] = {};
                for (let param in value) {
                    eeprom[key][param] = value[param]();
                }
            }
            return eeprom;
        }

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

        self.onAllBound = function () {
            OctoPrint.simpleApiGet("eeprom_marlin").done(function (response) {
                eeprom_from_json(response);
                info_from_json(response);
                console.log(eeprom_to_json());
            });
        };
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: EEPROMMarlinViewModel,
        dependencies: ["settingsViewModel"],
        elements: ["#tab_plugin_eeprom_marlin_2"],
    });
});
