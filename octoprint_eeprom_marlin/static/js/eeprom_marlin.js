/**
 * Created by Salandora on 27.07.2015.
 */
$(function() {
    function EepromMarlinViewModel(parameters) {
        var self = this;

        self.control = parameters[0];
        self.connection = parameters[1];

        self.firmwareRegEx = /FIRMWARE_NAME:([^\s]+)/i;
        self.marlinRegEx = /Marlin V[^\s]*/i;

        self.eepromDataRegEx = /EPR:(\d+) (\d+) ([^\s]+) (.+)/;

        self.isMarlinFirmware = ko.observable(false);

        self.isConnected = ko.computed(function() {
            return self.connection.isOperational() || self.connection.isPrinting() ||
                   self.connection.isReady() || self.connection.isPaused();
        });

        self.eepromData = ko.observableArray([]);

        self.onStartup = function() {
            $('#settings_plugin_eeprom_marlin_link a').on('show', function(e) {
                if (self.isConnected() && !self.isMarlinFirmware())
                    self._requestFirmwareInfo();
            });
        }

        self.fromHistoryData = function(data) {
            _.each(data.logs, function(line) {
                var match = self.firmwareRegEx.exec(line);
                if (match != null) {
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
                        if (self.marlinRegEx.exec(match[0]))
                            self.isMarlinFirmware(true);
                    }
                });
            }
            else
            {
                _.each(data.logs, function (line) {
                    var match = self.eepromDataRegEx.exec(line);
                    if (match) {
                        self.eepromData.push({
                            dataType: match[1],
                            position: match[2],
                            origValue: match[3],
                            value: match[3],
                            description: match[4]
                        });
                    }
                });
            }
        };

        self.onEventConnected = function() {
            self._requestFirmwareInfo();
        }

        self.onEventDisconnected = function() {
            self.isMarlinFirmware(false);
        };

        self.loadEeprom = function() {
            self.eepromData([]);
            self._requestEepromData();
        };

        self.saveEeprom = function()  {
            var eepromData = self.eepromData();
            _.each(eepromData, function(data) {
                if (data.origValue != data.value) {
                    self._requestSaveDataToEeprom(data.dataType, data.position, data.value);
                    data.origValue = data.value;
                }
            });
        };

        self._requestFirmwareInfo = function() {
            self.control.sendCustomCommand({ command: "M115" });
        };

        self._requestEepromData = function() {
            self.control.sendCustomCommand({ command: "M503" });
        }
        self._requestSaveDataToEeprom = function(data_type, position, value) {
            var cmd = "M206 T" + data_type + " P" + position;
            if (data_type == 3) {
                cmd += " X" + value;
                self.control.sendCustomCommand({ command: cmd });
            }
            else {
                cmd += " S" + value;
                self.control.sendCustomCommand({ command: cmd });
            }
        }
    }

    OCTOPRINT_VIEWMODELS.push([
        EepromMarlinViewModel,
        ["controlViewModel", "connectionViewModel"],
        "#settings_plugin_eeprom_marlin"
    ]);
});
