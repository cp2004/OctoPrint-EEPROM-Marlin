/**
* Created by Salandora on 27.07.2015.
* Modified by Anderson Silva on 01.04.2017.
*/
$(function() {
    function EepromMarlinViewModel(parameters) {
        var self = this;

        self.setRegExVars = function(version) {
            // All versions
            self.eepromM92RegEx = /M92 ([X])(.*)[^0-9]([Y])(.*)[^0-9]([Z])(.*)[^0-9]([E])(.*)/;
            self.eepromM203RegEx = /M203 ([X])(.*)[^0-9]([Y])(.*)[^0-9]([Z])(.*)[^0-9]([E])(.*)/;
            self.eepromM201RegEx = /M201 ([X])(.*)[^0-9]([Y])(.*)[^0-9]([Z])(.*)[^0-9]([E])(.*)/;
            self.eepromM206RegEx = /M206 ([X])(.*)[^0-9]([Y])(.*)[^0-9]([Z])(.*)/;
            self.eepromM851RegEx = /M851 ([Z])(.*)/;
            self.eepromM200RegEx = /M200 ([D])(.*)/;
            self.eepromM304RegEx = /M304 ([P])(.*)[^0-9]([I])(.*)[^0-9]([D])(.*)/;

            // Specific versions
            if (version == 'lastest' || version == 'Marlin 1.1.0-RC8') {
                self.eepromM205RegEx = /M205 ([S])(.*)[^0-9]([T])(.*)[^0-9]([B])(.*)[^0-9]([X])(.*)[^0-9]([Y])(.*)[^0-9]([Z])(.*)[^0-9]([E])(.*)/;
                self.eepromM145S0RegEx = /M145 S0 ([H])(.*)[^0-9]([B])(.*)[^0-9]([F])(.*)/;
                self.eepromM145S1RegEx = /M145 S1 ([H])(.*)[^0-9]([B])(.*)[^0-9]([F])(.*)/;
                self.eepromM145S2RegEx = /M145 S2 ([H])(.*)[^0-9]([B])(.*)[^0-9]([F])(.*)/;
                self.eepromM301RegEx = /M301 ([P])(.*)[^0-9]([I])(.*)[^0-9]([D])(.*)/;
                self.eepromM204RegEx = /M204 ([P])(.*)[^0-9]([R])(.*)[^0-9]([T])(.*)/;
            } else if (version == 'Marlin 1.1.0-RC1' || version == 'Marlin 1.1.0-RC2' || version == 'Marlin 1.1.0-RC3' || version == 'Marlin 1.1.0-RC4' || version == 'Marlin 1.1.0-RC5' || version == 'Marlin 1.1.0-RC6' || version == 'Marlin 1.1.0-RC7') {
                self.eepromM205RegEx = /M205 ([S])(.*)[^0-9]([T])(.*)[^0-9]([B])(.*)[^0-9]([X])(.*)[^0-9]([Z])(.*)[^0-9]([E])(.*)/;
                self.eepromM145S0RegEx = /M145 M0 ([H])(.*)[^0-9]([B])(.*)[^0-9]([F])(.*)/;
                self.eepromM145S1RegEx = /M145 M1 ([H])(.*)[^0-9]([B])(.*)[^0-9]([F])(.*)/;
                self.eepromM145S2RegEx = /M145 M2 ([H])(.*)[^0-9]([B])(.*)[^0-9]([F])(.*)/;
                self.eepromM301RegEx = /M301 ([P])(.*)[^0-9]([I])(.*)[^0-9]([D])(.*)[^0-9]([C])(.*)[^0-9]([L])(.*)/;
                self.eepromM204RegEx = /M204 ([P])(.*)[^0-9]([R])(.*)[^0-9]([T])(.*)/;
            } else if (version == 'Marlin 1.0.2+' || version == 'Marlin V1.0.2;' || version == 'Marlin 1.0.2') {
                self.eepromM204RegEx = /M204 ([S])(.*)[^0-9]([T])(.*)/;
                self.eepromM205RegEx = /M205 ([S])(.*)[^0-9]([T])(.*)[^0-9]([B])(.*)[^0-9]([X])(.*)[^0-9]([Z])(.*)[^0-9]([E])(.*)/;
                self.eepromM301RegEx = /M301 ([P])(.*)[^0-9]([I])(.*)[^0-9]([D])(.*)/;
            } else {
                self.eepromM205RegEx = /M205 ([S])(.*)[^0-9]([T])(.*)[^0-9]([B])(.*)[^0-9]([X])(.*)[^0-9]([Y])(.*)[^0-9]([Z])(.*)[^0-9]([E])(.*)/;
                self.eepromM145S0RegEx = /M145 S0 ([H])(.*)[^0-9]([B])(.*)[^0-9]([F])(.*)/;
                self.eepromM145S1RegEx = /M145 S1 ([H])(.*)[^0-9]([B])(.*)[^0-9]([F])(.*)/;
                self.eepromM145S2RegEx = /M145 S2 ([H])(.*)[^0-9]([B])(.*)[^0-9]([F])(.*)/;
                self.eepromM301RegEx = /M301 ([P])(.*)[^0-9]([I])(.*)[^0-9]([D])(.*)/;
                self.eepromM204RegEx = /M204 ([P])(.*)[^0-9]([R])(.*)[^0-9]([T])(.*)/;
            }
        };

        self.control = parameters[0];
        self.connection = parameters[1];
        self.FIRMWARE_NAME = ko.observable("");

        self.firmwareRegEx = /FIRMWARE_NAME:([^\s]*) ([^\s]*)/i;
        self.marlinRegEx = /Marlin[^\s]*/i;

        self.setRegExVars('lastest');

        self.isMarlinFirmware = ko.observable(false);

        self.isConnected = ko.computed(function() {
            return self.connection.isOperational() || self.connection.isPrinting() ||
            self.connection.isReady() || self.connection.isPaused();
        });

        self.eepromData1 = ko.observableArray([]);
        self.eepromData2 = ko.observableArray([]);
        self.eepromDataSteps = ko.observableArray([]);
        self.eepromDataFRates = ko.observableArray([]);
        self.eepromDataMaxAccel = ko.observableArray([]);
        self.eepromDataAccel = ko.observableArray([]);
        self.eepromDataPID = ko.observableArray([]);
        self.eepromDataPIDB = ko.observableArray([]);
        self.eepromDataHoming = ko.observableArray([]);
        self.eepromDataMaterialHS0 = ko.observableArray([]);
        self.eepromDataMaterialHS1 = ko.observableArray([]);
        self.eepromDataMaterialHS2 = ko.observableArray([]);
        self.eepromDataFilament = ko.observableArray([]);

        self.onStartup = function() {
            $('#settings_plugin_eeprom_marlin_link a').on('show', function(e) {
                if (self.isConnected() && !self.isMarlinFirmware()) {
                    self._requestFirmwareInfo();
                }
            });
        };

        self.firmware_name = function() {
            return self.FIRMWARE_NAME();
        };

        self.eepromFieldParse = function(line) {
            // M92 steps per unit
            var match = self.eepromM92RegEx.exec(line);
            if (match) {
                self.eepromDataSteps.push({
                    dataType: 'M92 X',
                    label: 'X axis',
                    origValue: match[2],
                    value: match[2],
                    unit: 'mm',
                    description: 'steps per unit'
                });

                self.eepromDataSteps.push({
                    dataType: 'M92 Y',
                    label: 'Y axis',
                    origValue: match[4],
                    value: match[4],
                    unit: 'mm',
                    description: 'steps per unit'
                });

                self.eepromDataSteps.push({
                    dataType: 'M92 Z',
                    label: 'Z axis',
                    origValue: match[6],
                    value: match[6],
                    unit: 'mm',
                    description: 'steps per unit'
                });

                self.eepromDataSteps.push({
                    dataType: 'M92 E',
                    label: 'Extruder',
                    origValue: match[8],
                    value: match[8],
                    unit: 'mm',
                    description: 'steps per unit'
                });
            }

            // M203 feedrates
            match = self.eepromM203RegEx.exec(line);
            if (match) {
                self.eepromDataFRates.push({
                    dataType: 'M203 X',
                    label: 'X axis',
                    origValue: match[2],
                    value: match[2],
                    unit: 'mm',
                    description: 'rate per unit'
                });

                self.eepromDataFRates.push({
                    dataType: 'M203 Y',
                    label: 'Y axis',
                    origValue: match[4],
                    value: match[4],
                    unit: 'mm',
                    description: 'rate per unit'
                });

                self.eepromDataFRates.push({
                    dataType: 'M203 Z',
                    label: 'Z axis',
                    origValue: match[6],
                    value: match[6],
                    unit: 'mm',
                    description: 'rate per unit'
                });

                self.eepromDataFRates.push({
                    dataType: 'M203 E',
                    label: 'Extruder',
                    origValue: match[8],
                    value: match[8],
                    unit: 'mm',
                    description: 'rate per unit'
                });
            }

            // M201 Maximum Acceleration (mm/s2)
            match = self.eepromM201RegEx.exec(line);
            if (match) {
                self.eepromDataMaxAccel.push({
                    dataType: 'M201 X',
                    label: 'X axis',
                    origValue: match[2],
                    value: match[2],
                    unit: 'mm/s2',
                    description: ''
                });

                self.eepromDataMaxAccel.push({
                    dataType: 'M201 Y',
                    label: 'Y axis',
                    origValue: match[4],
                    value: match[4],
                    unit: 'mm/s2',
                    description: ''
                });

                self.eepromDataMaxAccel.push({
                    dataType: 'M201 Z',
                    label: 'Z axis',
                    origValue: match[6],
                    value: match[6],
                    unit: 'mm/s2',
                    description: ''
                });

                self.eepromDataMaxAccel.push({
                    dataType: 'M201 E',
                    label: 'Extruder',
                    origValue: match[8],
                    value: match[8],
                    unit: 'mm/s2',
                    description: ''
                });
            }

            // M851 Z-Probe Offset
            match = self.eepromM851RegEx.exec(line);
            if (match) {
                self.eepromData1.push({
                    dataType: 'M851 Z',
                    label: 'Z-Probe Offset',
                    origValue: match[2],
                    value: match[2],
                    unit: 'mm',
                    description: ''
                });
            }

            // M206 Home offset
            match = self.eepromM206RegEx.exec(line);
            if (match) {
                self.eepromDataHoming.push({
                    dataType: 'M206 X',
                    label: 'X axis',
                    origValue: match[2],
                    value: match[2],
                    unit: 'mm',
                    description: ''
                });

                self.eepromDataHoming.push({
                    dataType: 'M206 Y',
                    label: 'Y axis',
                    origValue: match[4],
                    value: match[4],
                    unit: 'mm',
                    description: ''
                });

                self.eepromDataHoming.push({
                    dataType: 'M206 Z',
                    label: 'Z axis',
                    origValue: match[6],
                    value: match[6],
                    unit: 'mm',
                    description: ''
                });
            }

            // Filament diameter
            match = self.eepromM200RegEx.exec(line);
            if (match) {
                if (self.eepromDataFilament().length === 0) {
                    self.eepromDataFilament.push({
                        dataType: 'M200 D',
                        label: 'Diameter',
                        origValue: match[2],
                        value: match[2],
                        unit: 'mm',
                        description: ''
                    });
                }
            }

            // M304 PID settings
            match = self.eepromM304RegEx.exec(line);
            if (match) {
                self.eepromDataPIDB.push({
                    dataType: 'M304 P',
                    label: 'Bed Kp',
                    origValue: match[2],
                    value: match[2],
                    unit: 'term',
                    description: ''
                });

                self.eepromDataPIDB.push({
                    dataType: 'M304 I',
                    label: 'Ki',
                    origValue: match[4],
                    value: match[4],
                    unit: 'term',
                    description: ''
                });

                self.eepromDataPIDB.push({
                    dataType: 'M304 D',
                    label: 'Kd',
                    origValue: match[6],
                    value: match[6],
                    unit: 'term',
                    description: ''
                });
            }

            if (self.firmware_name() == 'Marlin 1.1.0-RC8') {
                // M205 Advanced variables
                match = self.eepromM205RegEx.exec(line);
                if (match) {
                    self.eepromData1.push({
                        dataType: 'M205 S',
                        label: 'Min feedrate',
                        origValue: match[2],
                        value: match[2],
                        unit: 'mm/s',
                        description: ''
                    });

                    self.eepromData1.push({
                        dataType: 'M205 T',
                        label: 'Min travel',
                        origValue: match[4],
                        value: match[4],
                        unit: 'mm/s',
                        description: ''
                    });

                    self.eepromData1.push({
                        dataType: 'M205 B',
                        label: 'Min segment',
                        origValue: match[6],
                        value: match[6],
                        unit: 'mm/s',
                        description: ''
                    });

                    self.eepromData2.push({
                        dataType: 'M205 X',
                        label: 'Max X jerk',
                        origValue: match[8],
                        value: match[8],
                        unit: 'mm/s',
                        description: ''
                    });

                    self.eepromData2.push({
                        dataType: 'M205 Y',
                        label: 'Max Y jerk',
                        origValue: match[8],
                        value: match[8],
                        unit: 'mm/s',
                        description: ''
                    });

                    self.eepromData2.push({
                        dataType: 'M205 Z',
                        label: 'Max Z jerk',
                        origValue: match[10],
                        value: match[10],
                        unit: 'mm/s',
                        description: ''
                    });

                    self.eepromData2.push({
                        dataType: 'M205 E',
                        label: 'Max E jerk',
                        origValue: match[12],
                        value: match[12],
                        unit: 'mm/s',
                        description: ''
                    });
                }

                // M204 Acceleration
                match = self.eepromM204RegEx.exec(line);
                if (match) {
                    self.eepromDataAccel.push({
                        dataType: 'M204 P',
                        label: 'Printing moves',
                        origValue: match[2],
                        value: match[2],
                        unit: 'mm/s2',
                        description: ''
                    });

                    self.eepromDataAccel.push({
                        dataType: 'M204 R',
                        label: 'Retract',
                        origValue: match[4],
                        value: match[4],
                        unit: 'mm/s2',
                        description: ''
                    });

                    self.eepromDataAccel.push({
                        dataType: 'M204 T',
                        label: 'Travel',
                        origValue: match[6],
                        value: match[6],
                        unit: 'mm/s2',
                        description: ''
                    });
                }

                // M301 PID settings
                match = self.eepromM301RegEx.exec(line);
                if (match) {
                    self.eepromDataPID.push({
                        dataType: 'M301 P',
                        label: 'Hotend Kp',
                        origValue: match[2],
                        value: match[2],
                        unit: 'term',
                        description: ''
                    });

                    self.eepromDataPID.push({
                        dataType: 'M301 I',
                        label: 'Ki',
                        origValue: match[4],
                        value: match[4],
                        unit: 'term',
                        description: ''
                    });

                    self.eepromDataPID.push({
                        dataType: 'M301 D',
                        label: 'Kd',
                        origValue: match[6],
                        value: match[6],
                        unit: 'term',
                        description: ''
                    });
                }

                // M145 Material heatup
                match = self.eepromM145S0RegEx.exec(line);
                if (match) {
                    self.eepromDataMaterialHS0.push({
                        dataType: 'M145 S0 H',
                        label: 'S0 Hotend Temperature',
                        origValue: match[2],
                        value: match[2],
                        unit: '',
                        description: ''
                    });
                    self.eepromDataMaterialHS0.push({
                        dataType: 'M145 S0 B',
                        label: 'Bed Temperature',
                        origValue: match[4],
                        value: match[4],
                        unit: '',
                        description: ''
                    });
                    self.eepromDataMaterialHS0.push({
                        dataType: 'M145 S0 F',
                        label: 'Fan Speed',
                        origValue: match[6],
                        value: match[6],
                        unit: '',
                        description: ''
                    });
                }

                match = self.eepromM145S1RegEx.exec(line);
                if (match) {
                    self.eepromDataMaterialHS1.push({
                        dataType: 'M145 S1 H',
                        label: 'S1 Hotend Temperature',
                        origValue: match[2],
                        value: match[2],
                        unit: '',
                        description: ''
                    });
                    self.eepromDataMaterialHS1.push({
                        dataType: 'M145 S1 B',
                        label: 'Bed Temperature',
                        origValue: match[4],
                        value: match[4],
                        unit: '',
                        description: ''
                    });
                    self.eepromDataMaterialHS1.push({
                        dataType: 'M145 S1 F',
                        label: 'Fan Speed',
                        origValue: match[6],
                        value: match[6],
                        unit: '',
                        description: ''
                    });
                }

                match = self.eepromM145S2RegEx.exec(line);
                if (match) {
                    self.eepromDataMaterialHS2.push({
                        dataType: 'M145 S2 H',
                        label: 'S2 Hotend Temperature',
                        origValue: match[2],
                        value: match[2],
                        unit: '',
                        description: ''
                    });
                    self.eepromDataMaterialHS2.push({
                        dataType: 'M145 S2 B',
                        label: 'Bed Temperature',
                        origValue: match[4],
                        value: match[4],
                        unit: '',
                        description: ''
                    });
                    self.eepromDataMaterialHS2.push({
                        dataType: 'M145 S2 F',
                        label: 'Fan Speed',
                        origValue: match[6],
                        value: match[6],
                        unit: '',
                        description: ''
                    });
                }
            } else if (self.firmware_name() == 'Marlin 1.1.0-RC1' || self.firmware_name() == 'Marlin 1.1.0-RC2' || self.firmware_name() == 'Marlin 1.1.0-RC3' || self.firmware_name() == 'Marlin 1.1.0-RC4' || self.firmware_name() == 'Marlin 1.1.0-RC5' || self.firmware_name() == 'Marlin 1.1.0-RC6' || self.firmware_name() == 'Marlin 1.1.0-RC7') {
                // M205 Advanced variables
                match = self.eepromM205RegEx.exec(line);
                if (match) {
                    self.eepromData1.push({
                        dataType: 'M205 S',
                        label: 'Min feedrate',
                        origValue: match[2],
                        value: match[2],
                        unit: 'mm/s',
                        description: ''
                    });

                    self.eepromData1.push({
                        dataType: 'M205 T',
                        label: 'Min travel',
                        origValue: match[4],
                        value: match[4],
                        unit: 'mm/s',
                        description: ''
                    });

                    self.eepromData1.push({
                        dataType: 'M205 B',
                        label: 'Min segment',
                        origValue: match[6],
                        value: match[6],
                        unit: 'mm/s',
                        description: ''
                    });

                    self.eepromData2.push({
                        dataType: 'M205 X',
                        label: 'Max X jerk',
                        origValue: match[8],
                        value: match[8],
                        unit: 'mm/s',
                        description: ''
                    });

                    self.eepromData2.push({
                        dataType: 'M205 Y',
                        label: 'Max Y jerk',
                        origValue: match[8],
                        value: match[8],
                        unit: 'mm/s',
                        description: ''
                    });

                    self.eepromData2.push({
                        dataType: 'M205 Z',
                        label: 'Max Z jerk',
                        origValue: match[10],
                        value: match[10],
                        unit: 'mm/s',
                        description: ''
                    });

                    self.eepromData2.push({
                        dataType: 'M205 E',
                        label: 'Max E jerk',
                        origValue: match[12],
                        value: match[12],
                        unit: 'mm/s',
                        description: ''
                    });
                }

                // M204 Acceleration
                match = self.eepromM204RegEx.exec(line);
                if (match) {
                    self.eepromDataAccel.push({
                        dataType: 'M204 P',
                        label: 'Printing moves',
                        origValue: match[2],
                        value: match[2],
                        unit: 'mm/s2',
                        description: ''
                    });

                    self.eepromDataAccel.push({
                        dataType: 'M204 R',
                        label: 'Retract',
                        origValue: match[4],
                        value: match[4],
                        unit: 'mm/s2',
                        description: ''
                    });

                    self.eepromDataAccel.push({
                        dataType: 'M204 T',
                        label: 'Travel',
                        origValue: match[6],
                        value: match[6],
                        unit: 'mm/s2',
                        description: ''
                    });
                }

                // M301 PID settings
                match = self.eepromM301RegEx.exec(line);
                if (match) {
                    self.eepromDataPID.push({
                        dataType: 'M301 P',
                        label: 'Hotend Kp',
                        origValue: match[2],
                        value: match[2],
                        unit: 'term',
                        description: ''
                    });

                    self.eepromDataPID.push({
                        dataType: 'M301 I',
                        label: 'Ki',
                        origValue: match[4],
                        value: match[4],
                        unit: 'term',
                        description: ''
                    });

                    self.eepromDataPID.push({
                        dataType: 'M301 D',
                        label: 'Kd',
                        origValue: match[6],
                        value: match[6],
                        unit: 'term',
                        description: ''
                    });

                    self.eepromDataPID.push({
                        dataType: 'M301 C',
                        label: 'Kc',
                        origValue: match[8],
                        value: match[8],
                        unit: 'term',
                        description: ''
                    });

                    self.eepromDataPID.push({
                        dataType: 'M301 L',
                        label: 'LPQ',
                        origValue: match[10],
                        value: match[10],
                        unit: 'len',
                        description: ''
                    });
                }

                // M145 Material heatup
                match = self.eepromM145S0RegEx.exec(line);
                if (match) {
                    self.eepromDataMaterialHS0.push({
                        dataType: 'M145 M0 H',
                        label: 'M0 Hotend Temperature',
                        origValue: match[2],
                        value: match[2],
                        unit: '',
                        description: ''
                    });
                    self.eepromDataMaterialHS0.push({
                        dataType: 'M145 M0 B',
                        label: 'Bed Temperature',
                        origValue: match[4],
                        value: match[4],
                        unit: '',
                        description: ''
                    });
                    self.eepromDataMaterialHS0.push({
                        dataType: 'M145 M0 F',
                        label: 'Fan Speed',
                        origValue: match[6],
                        value: match[6],
                        unit: '',
                        description: ''
                    });
                }

                match = self.eepromM145S1RegEx.exec(line);
                if (match) {
                    self.eepromDataMaterialHS1.push({
                        dataType: 'M145 M1 H',
                        label: 'M1 Hotend Temperature',
                        origValue: match[2],
                        value: match[2],
                        unit: '',
                        description: ''
                    });
                    self.eepromDataMaterialHS1.push({
                        dataType: 'M145 M1 B',
                        label: 'Bed Temperature',
                        origValue: match[4],
                        value: match[4],
                        unit: '',
                        description: ''
                    });
                    self.eepromDataMaterialHS1.push({
                        dataType: 'M145 M1 F',
                        label: 'Fan Speed',
                        origValue: match[6],
                        value: match[6],
                        unit: '',
                        description: ''
                    });
                }

                match = self.eepromM145S2RegEx.exec(line);
                if (match) {
                    self.eepromDataMaterialHS2.push({
                        dataType: 'M145 M2 H',
                        label: 'M2 Hotend Temperature',
                        origValue: match[2],
                        value: match[2],
                        unit: '',
                        description: ''
                    });
                    self.eepromDataMaterialHS2.push({
                        dataType: 'M145 M2 B',
                        label: 'Bed Temperature',
                        origValue: match[4],
                        value: match[4],
                        unit: '',
                        description: ''
                    });
                    self.eepromDataMaterialHS2.push({
                        dataType: 'M145 M2 F',
                        label: 'Fan Speed',
                        origValue: match[6],
                        value: match[6],
                        unit: '',
                        description: ''
                    });
                }
            } else if (self.firmware_name() == 'Marlin 1.0.2+' || self.firmware_name() == 'Marlin V1.0.2;' || self.firmware_name() == 'Marlin 1.0.2') {
                // M205 Advanced variables
                match = self.eepromM205RegEx.exec(line);
                if (match) {
                    self.eepromData1.push({
                        dataType: 'M205 S',
                        label: 'Min feedrate',
                        origValue: match[2],
                        value: match[2],
                        unit: 'mm/s',
                        description: ''
                    });

                    self.eepromData1.push({
                        dataType: 'M205 T',
                        label: 'Min travel',
                        origValue: match[4],
                        value: match[4],
                        unit: 'mm/s',
                        description: ''
                    });

                    self.eepromData1.push({
                        dataType: 'M205 B',
                        label: 'Min segment',
                        origValue: match[6],
                        value: match[6],
                        unit: 'mm/s',
                        description: ''
                    });

                    self.eepromData2.push({
                        dataType: 'M205 X',
                        label: 'Max X jerk',
                        origValue: match[8],
                        value: match[8],
                        unit: 'mm/s',
                        description: ''
                    });

                    self.eepromData2.push({
                        dataType: 'M205 Z',
                        label: 'Max Z jerk',
                        origValue: match[10],
                        value: match[10],
                        unit: 'mm/s',
                        description: ''
                    });

                    self.eepromData2.push({
                        dataType: 'M205 E',
                        label: 'Max E jerk',
                        origValue: match[12],
                        value: match[12],
                        unit: 'mm/s',
                        description: ''
                    });
                }

                // M204 Acceleration
                match = self.eepromM204RegEx.exec(line);
                if (match) {
                    self.eepromDataAccel.push({
                        dataType: 'M204 S',
                        label: 'Printing moves',
                        origValue: match[2],
                        value: match[2],
                        unit: 'mm/s2',
                        description: ''
                    });

                    self.eepromDataAccel.push({
                        dataType: 'M204 T',
                        label: 'Travel',
                        origValue: match[4],
                        value: match[4],
                        unit: 'mm/s2',
                        description: ''
                    });
                }

                // M301 PID settings
                match = self.eepromM301RegEx.exec(line);
                if (match) {
                    self.eepromDataPID.push({
                        dataType: 'M301 P',
                        label: 'Hotend Kp',
                        origValue: match[2],
                        value: match[2],
                        unit: 'term',
                        description: ''
                    });

                    self.eepromDataPID.push({
                        dataType: 'M301 I',
                        label: 'Ki',
                        origValue: match[4],
                        value: match[4],
                        unit: 'term',
                        description: ''
                    });

                    self.eepromDataPID.push({
                        dataType: 'M301 D',
                        label: 'Kd',
                        origValue: match[6],
                        value: match[6],
                        unit: 'term',
                        description: ''
                    });
                }
            } else {
                // M205 Advanced variables
                match = self.eepromM205RegEx.exec(line);
                if (match) {
                    self.eepromData1.push({
                        dataType: 'M205 S',
                        label: 'Min feedrate',
                        origValue: match[2],
                        value: match[2],
                        unit: 'mm/s',
                        description: ''
                    });

                    self.eepromData1.push({
                        dataType: 'M205 T',
                        label: 'Min travel',
                        origValue: match[4],
                        value: match[4],
                        unit: 'mm/s',
                        description: ''
                    });

                    self.eepromData1.push({
                        dataType: 'M205 B',
                        label: 'Min segment',
                        origValue: match[6],
                        value: match[6],
                        unit: 'mm/s',
                        description: ''
                    });

                    self.eepromData2.push({
                        dataType: 'M205 X',
                        label: 'Max X jerk',
                        origValue: match[8],
                        value: match[8],
                        unit: 'mm/s',
                        description: ''
                    });

                    self.eepromData2.push({
                        dataType: 'M205 Y',
                        label: 'Max Y jerk',
                        origValue: match[8],
                        value: match[8],
                        unit: 'mm/s',
                        description: ''
                    });

                    self.eepromData2.push({
                        dataType: 'M205 Z',
                        label: 'Max Z jerk',
                        origValue: match[10],
                        value: match[10],
                        unit: 'mm/s',
                        description: ''
                    });

                    self.eepromData2.push({
                        dataType: 'M205 E',
                        label: 'Max E jerk',
                        origValue: match[12],
                        value: match[12],
                        unit: 'mm/s',
                        description: ''
                    });
                }

                // M204 Acceleration
                match = self.eepromM204RegEx.exec(line);
                if (match) {
                    self.eepromDataAccel.push({
                        dataType: 'M204 P',
                        label: 'Printing moves',
                        origValue: match[2],
                        value: match[2],
                        unit: 'mm/s2',
                        description: ''
                    });

                    self.eepromDataAccel.push({
                        dataType: 'M204 R',
                        label: 'Retract',
                        origValue: match[4],
                        value: match[4],
                        unit: 'mm/s2',
                        description: ''
                    });

                    self.eepromDataAccel.push({
                        dataType: 'M204 T',
                        label: 'Travel',
                        origValue: match[6],
                        value: match[6],
                        unit: 'mm/s2',
                        description: ''
                    });
                }

                // M301 PID settings
                match = self.eepromM301RegEx.exec(line);
                if (match) {
                    self.eepromDataPID.push({
                        dataType: 'M301 P',
                        label: 'Hotend Kp',
                        origValue: match[2],
                        value: match[2],
                        unit: 'term',
                        description: ''
                    });

                    self.eepromDataPID.push({
                        dataType: 'M301 I',
                        label: 'Ki',
                        origValue: match[4],
                        value: match[4],
                        unit: 'term',
                        description: ''
                    });

                    self.eepromDataPID.push({
                        dataType: 'M301 D',
                        label: 'Kd',
                        origValue: match[6],
                        value: match[6],
                        unit: 'term',
                        description: ''
                    });
                }

                // M145 Material heatup
                match = self.eepromM145S0RegEx.exec(line);
                if (match) {
                    self.eepromDataMaterialHS0.push({
                        dataType: 'M145 S0 H',
                        label: 'S0 Hotend Temperature',
                        origValue: match[2],
                        value: match[2],
                        unit: '',
                        description: ''
                    });
                    self.eepromDataMaterialHS0.push({
                        dataType: 'M145 S0 B',
                        label: 'Bed Temperature',
                        origValue: match[4],
                        value: match[4],
                        unit: '',
                        description: ''
                    });
                    self.eepromDataMaterialHS0.push({
                        dataType: 'M145 S0 F',
                        label: 'Fan Speed',
                        origValue: match[6],
                        value: match[6],
                        unit: '',
                        description: ''
                    });
                }

                match = self.eepromM145S1RegEx.exec(line);
                if (match) {
                    self.eepromDataMaterialHS1.push({
                        dataType: 'M145 S1 H',
                        label: 'S1 Hotend Temperature',
                        origValue: match[2],
                        value: match[2],
                        unit: '',
                        description: ''
                    });
                    self.eepromDataMaterialHS1.push({
                        dataType: 'M145 S1 B',
                        label: 'Bed Temperature',
                        origValue: match[4],
                        value: match[4],
                        unit: '',
                        description: ''
                    });
                    self.eepromDataMaterialHS1.push({
                        dataType: 'M145 S1 F',
                        label: 'Fan Speed',
                        origValue: match[6],
                        value: match[6],
                        unit: '',
                        description: ''
                    });
                }

                match = self.eepromM145S2RegEx.exec(line);
                if (match) {
                    self.eepromDataMaterialHS2.push({
                        dataType: 'M145 S2 H',
                        label: 'S2 Hotend Temperature',
                        origValue: match[2],
                        value: match[2],
                        unit: '',
                        description: ''
                    });
                    self.eepromDataMaterialHS2.push({
                        dataType: 'M145 S2 B',
                        label: 'Bed Temperature',
                        origValue: match[4],
                        value: match[4],
                        unit: '',
                        description: ''
                    });
                    self.eepromDataMaterialHS2.push({
                        dataType: 'M145 S2 F',
                        label: 'Fan Speed',
                        origValue: match[6],
                        value: match[6],
                        unit: '',
                        description: ''
                    });
                }
            }
        };

        self.fromHistoryData = function(data) {
            _.each(data.logs, function(line) {
                var match = self.firmwareRegEx.exec(line);
                if (match !== null) {
                    self.FIRMWARE_NAME(match[1] + ' ' + match[2]);
                    self.setRegExVars(self.firmware_name());
                    console.debug('Firmware: ' + self.firmware_name());
                    console.debug(match);
                    console.debug(line);
                    if (self.marlinRegEx.exec(match[0]))
                    self.isMarlinFirmware(true);
                }
            });
        };

        self.fromCurrentData = function(data) {
            if (!self.isMarlinFirmware()) {
                _.each(data.logs, function (line) {
                    var match = self.firmwareRegEx.exec(line);
                    if (match) {
                        self.FIRMWARE_NAME(match[1] + ' ' + match[2]);
                        self.setRegExVars(self.firmware_name());
                        console.debug('Firmware: ' + self.firmware_name());
                        console.debug(match);
                        console.debug(line);
                        if (self.marlinRegEx.exec(match[0]))
                        self.isMarlinFirmware(true);
                    }
                });
            }
            else
            {
                _.each(data.logs, function (line) {
                    self.eepromFieldParse(line);
                });
            }
        };

        self.eepromDataCount = ko.computed(function() {
            return (self.eepromData1().length + self.eepromData2().length) > 0;
        });

        self.eepromDataStepsCount = ko.computed(function() {
            return self.eepromDataSteps().length > 0;
        });

        self.eepromDataFRatesCount = ko.computed(function() {
            return self.eepromDataFRates().length > 0;
        });

        self.eepromDataMaxAccelCount = ko.computed(function() {
            return self.eepromDataMaxAccel().length > 0;
        });

        self.eepromDataAccelCount = ko.computed(function() {
            return self.eepromDataAccel().length > 0;
        });

        self.eepromDataPIDCount = ko.computed(function() {
            return (self.eepromDataPID().length + self.eepromDataPIDB().length) > 0;
        });

        self.eepromDataHomingCount = ko.computed(function() {
            return self.eepromDataHoming().length > 0;
        });

        self.eepromDataMaterialCount = ko.computed(function() {
            return (self.eepromDataMaterialHS0().length + self.eepromDataMaterialHS1().length + self.eepromDataMaterialHS2().length) > 0;
        });

        self.eepromDataFilamentCount = ko.computed(function() {
            return self.eepromDataFilament().length > 0;
        });

        self.onEventConnected = function() {
            self._requestFirmwareInfo();
            setTimeout(function() {self.loadEeprom(); }, 5000);
        };

        self.onStartupComplete = function() {
            setTimeout(function() {self.loadEeprom(); }, 5000);
        };

        self.onEventDisconnected = function() {
            self.isMarlinFirmware(false);
        };

        self.loadEeprom = function() {
            self.eepromData1([]);
            self.eepromData2([]);
            self.eepromDataSteps([]);
            self.eepromDataFRates([]);
            self.eepromDataMaxAccel([]);
            self.eepromDataAccel([]);
            self.eepromDataPID([]);
            self.eepromDataPIDB([]);
            self.eepromDataHoming([]);
            self.eepromDataMaterialHS0([]);
            self.eepromDataMaterialHS1([]);
            self.eepromDataMaterialHS2([]);
            self.eepromDataFilament([]);

            self._requestEepromData();
        };

        self.saveEeprom = function()  {
            var cmd = 'M500';
            var eepromData = self.eepromData1();
            _.each(eepromData, function(data) {
                if (data.origValue != data.value) {
                    self._requestSaveDataToEeprom(data.dataType, data.value);
                    data.origValue = data.value;
                }
            });

            eepromData = self.eepromData2();
            _.each(eepromData, function(data) {
                if (data.origValue != data.value) {
                    self._requestSaveDataToEeprom(data.dataType, data.value);
                    data.origValue = data.value;
                }
            });

            eepromData = self.eepromDataSteps();
            _.each(eepromData, function(data) {
                if (data.origValue != data.value) {
                    self._requestSaveDataToEeprom(data.dataType, data.value);
                    data.origValue = data.value;
                }
            });

            eepromData = self.eepromDataFRates();
            _.each(eepromData, function(data) {
                if (data.origValue != data.value) {
                    self._requestSaveDataToEeprom(data.dataType, data.value);
                    data.origValue = data.value;
                }
            });

            eepromData = self.eepromDataMaxAccel();
            _.each(eepromData, function(data) {
                if (data.origValue != data.value) {
                    self._requestSaveDataToEeprom(data.dataType, data.value);
                    data.origValue = data.value;
                }
            });

            eepromData = self.eepromDataAccel();
            _.each(eepromData, function(data) {
                if (data.origValue != data.value) {
                    self._requestSaveDataToEeprom(data.dataType, data.value);
                    data.origValue = data.value;
                }
            });

            eepromData = self.eepromDataPID();
            _.each(eepromData, function(data) {
                if (data.origValue != data.value) {
                    self._requestSaveDataToEeprom(data.dataType, data.value);
                    data.origValue = data.value;
                }
            });

            eepromData = self.eepromDataPIDB();
            _.each(eepromData, function(data) {
                if (data.origValue != data.value) {
                    self._requestSaveDataToEeprom(data.dataType, data.value);
                    data.origValue = data.value;
                }
            });

            eepromData = self.eepromDataHoming();
            _.each(eepromData, function(data) {
                if (data.origValue != data.value) {
                    self._requestSaveDataToEeprom(data.dataType, data.value);
                    data.origValue = data.value;
                }
            });

            eepromData = self.eepromDataMaterialHS0();
            _.each(eepromData, function(data) {
                if (data.origValue != data.value) {
                    self._requestSaveDataToEeprom(data.dataType, data.value);
                    data.origValue = data.value;
                }
            });

            eepromData = self.eepromDataMaterialHS1();
            _.each(eepromData, function(data) {
                if (data.origValue != data.value) {
                    self._requestSaveDataToEeprom(data.dataType, data.value);
                    data.origValue = data.value;
                }
            });

            eepromData = self.eepromDataMaterialHS2();
            _.each(eepromData, function(data) {
                if (data.origValue != data.value) {
                    self._requestSaveDataToEeprom(data.dataType, data.value);
                    data.origValue = data.value;
                }
            });

            eepromData = self.eepromDataFilament();
            _.each(eepromData, function(data) {
                if (data.origValue != data.value) {
                    self._requestSaveDataToEeprom(data.dataType, data.value);
                    data.origValue = data.value;
                }
            });

            self.control.sendCustomCommand({ command: cmd });

            alert('EEPROM data stored.');
        };

        self._requestFirmwareInfo = function() {
            self.control.sendCustomCommand({ command: "M115" });
        };

        self._requestEepromData = function() {
            self.control.sendCustomCommand({ command: "M503" });
        };

        self._requestSaveDataToEeprom = function(data_type, value) {
            var cmd = data_type + value;
            self.control.sendCustomCommand({ command: cmd });
        };
    }

    OCTOPRINT_VIEWMODELS.push([
        EepromMarlinViewModel,
        ["controlViewModel", "connectionViewModel"],
        "#settings_plugin_eeprom_marlin"
    ]);
});
