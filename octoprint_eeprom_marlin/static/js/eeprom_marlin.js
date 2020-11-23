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

        function eeprom_from_dict(data) {
            // advanced
            self.eeprom.advanced.B(data.eeprom.advanced.params.B);
            self.eeprom.advanced.E(data.eeprom.advanced.params.E);
            self.eeprom.advanced.S(data.eeprom.advanced.params.S);
            self.eeprom.advanced.T(data.eeprom.advanced.params.T);
            self.eeprom.advanced.X(data.eeprom.advanced.params.X);
            self.eeprom.advanced.Y(data.eeprom.advanced.params.Y);
            self.eeprom.advanced.Z(data.eeprom.advanced.params.Z);
            // autolevel
            self.eeprom.autolevel.S(data.eeprom.autolevel.params.S);
            self.eeprom.autolevel.Z(data.eeprom.autolevel.params.Z);
            // bed_pid
            self.eeprom.bed_pid.D(data.eeprom.bed_pid.params.D);
            self.eeprom.bed_pid.I(data.eeprom.bed_pid.params.I);
            self.eeprom.bed_pid.P(data.eeprom.bed_pid.params.P);
            // delta
            self.eeprom.delta.A(data.eeprom.delta.params.A);
            self.eeprom.delta.B(data.eeprom.delta.params.B);
            self.eeprom.delta.C(data.eeprom.delta.params.C);
            self.eeprom.delta.L(data.eeprom.delta.params.L);
            self.eeprom.delta.R(data.eeprom.delta.params.R);
            self.eeprom.delta.S(data.eeprom.delta.params.S);
            // endstop
            self.eeprom.endstop.X(data.eeprom.endstop.params.X);
            self.eeprom.endstop.Y(data.eeprom.endstop.params.Y);
            self.eeprom.endstop.Z(data.eeprom.endstop.params.Z);
            // feedrate
            self.eeprom.feedrate.E(data.eeprom.feedrate.params.E);
            self.eeprom.feedrate.X(data.eeprom.feedrate.params.X);
            self.eeprom.feedrate.Y(data.eeprom.feedrate.params.Y);
            self.eeprom.feedrate.Z(data.eeprom.feedrate.params.Z);
            // filament
            self.eeprom.filament.D(data.eeprom.filament.params.D);
            // hotend_pid
            self.eeprom.hotend_pid.D(data.eeprom.hotend_pid.params.D);
            self.eeprom.hotend_pid.I(data.eeprom.hotend_pid.params.I);
            self.eeprom.hotend_pid.P(data.eeprom.hotend_pid.params.P);
            // linear
            self.eeprom.linear.K(data.eeprom.linear.params.K);
            self.eeprom.linear.R(data.eeprom.linear.params.R);
            // max_acceleration
            self.eeprom.max_acceleration.E(
                data.eeprom.max_acceleration.params.E
            );
            self.eeprom.max_acceleration.X(
                data.eeprom.max_acceleration.params.X
            );
            self.eeprom.max_acceleration.Y(
                data.eeprom.max_acceleration.params.Y
            );
            self.eeprom.max_acceleration.Z(
                data.eeprom.max_acceleration.params.Z
            );
            // print_acceleration
            self.eeprom.print_acceleration.P(
                data.eeprom.print_acceleration.params.P
            );
            self.eeprom.print_acceleration.R(
                data.eeprom.print_acceleration.params.R
            );
            self.eeprom.print_acceleration.T(
                data.eeprom.print_acceleration.params.T
            );
            // probe_offset
            self.eeprom.probe_offset.X(data.eeprom.probe_offset.params.X);
            self.eeprom.probe_offset.Y(data.eeprom.probe_offset.params.Y);
            self.eeprom.probe_offset.Z(data.eeprom.probe_offset.params.Z);
            // steps
            self.eeprom.steps.X(data.eeprom.steps.params.X);
            self.eeprom.steps.Y(data.eeprom.steps.params.Y);
            self.eeprom.steps.Z(data.eeprom.steps.params.Z);
            self.eeprom.steps.E(data.eeprom.steps.params.E);
        }

        function eeprom_to_dict() {
            var eeprom = {};
            // advanced
            eeprom.advanced.B = self.eeprom.advanced.B();
            eeprom.advanced.E = self.eeprom.advanced.E();
            eeprom.advanced.S = self.eeprom.advanced.S();
            eeprom.advanced.T = self.eeprom.advanced.T();
            eeprom.advanced.X = self.eeprom.advanced.X();
            eeprom.advanced.Y = self.eeprom.advanced.Y();
            eeprom.advanced.Z = self.eeprom.advanced.Z();
            // autolevel
            eeprom.autolevel.S = self.eeprom.autolevel.S();
            eeprom.autolevel.Z = self.eeprom.autolevel.Z();
            // bed_pid
            eeprom.bed_pid.D = self.eeprom.bed_pid.D();
            eeprom.bed_pid.I = self.eeprom.bed_pid.I();
            eeprom.bed_pid.P = self.eeprom.bed_pid.P();
            // delta
            eeprom.delta.A = self.eeprom.delta.A();
            eeprom.delta.B = self.eeprom.delta.B();
            eeprom.delta.C = self.eeprom.delta.C();
            eeprom.delta.L = self.eeprom.delta.L();
            eeprom.delta.R = self.eeprom.delta.R();
            eeprom.delta.S = self.eeprom.delta.S();
            // endstop
            eeprom.endstop.X = self.eeprom.endstop.X();
            eeprom.endstop.Y = self.eeprom.endstop.Y();
            eeprom.endstop.Z = self.eeprom.endstop.Z();
            // feedrate
            eeprom.feedrate.E = self.eeprom.feedrate.E();
            eeprom.feedrate.X = self.eeprom.feedrate.X();
            eeprom.feedrate.Y = self.eeprom.feedrate.Y();
            eeprom.feedrate.Z = self.eeprom.feedrate.Z();
            // filament
            eeprom.filament.D = self.eeprom.filament.D();
            // hotend_pid
            eeprom.hotend_pid.D = self.eeprom.hotend_pid.D();
            eeprom.hotend_pid.I = self.eeprom.hotend_pid.I();
            eeprom.hotend_pid.P = self.eeprom.hotend_pid.P();
            // linear
            eeprom.linear.K = self.eeprom.linear.K();
            eeprom.linear.R = self.eeprom.linear.R();
            // max_acceleration
            eeprom.max_acceleration.E = self.eeprom.max_acceleration.E();
            eeprom.max_acceleration.X = self.eeprom.max_acceleration.X();
            eeprom.max_acceleration.Y = self.eeprom.max_acceleration.Y();
            eeprom.max_acceleration.Z = self.eeprom.max_acceleration.Z();
            // print_acceleration
            eeprom.print_acceleration.P = self.eeprom.print_acceleration.P();
            eeprom.print_acceleration.R = self.eeprom.print_acceleration.R();
            eeprom.print_acceleration.T = self.eeprom.print_acceleration.T();
            // probe_offset
            eeprom.probe_offset.X = self.eeprom.probe_offset.X();
            eeprom.probe_offset.Y = self.eeprom.probe_offset.Y();
            eeprom.probe_offset.Z = self.eeprom.probe_offset.Z();
            // steps
            eeprom.steps.X = self.eeprom.steps.X();
            eeprom.steps.Y = self.eeprom.steps.Y();
            eeprom.steps.Z = self.eeprom.steps.Z();
            eeprom.steps.E = self.eeprom.steps.E();

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

        function info_from_dict(data) {
            self.info.additional(data.info.additional);
            self.info.capabilities(data.info.capabilities);
            self.info.is_marlin(data.info.is_marlin);
            self.info.name(data.info.name);
        }

        self.onAllBound = function () {
            OctoPrint.simpleApiGet("eeprom_marlin").done(function (response) {
                eeprom_from_dict(response);
                info_from_dict(response);
            });
        };
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: EEPROMMarlinViewModel,
        dependencies: ["settingsViewModel"],
        elements: ["#tab_plugin_eeprom_marlin_2"],
    });
});
