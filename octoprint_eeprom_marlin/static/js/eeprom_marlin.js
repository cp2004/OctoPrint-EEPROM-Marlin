/**
 * Plugin was Created by Salandora on 27.07.2015, Modified by Anderson Silva on 20.08.2017, Contribution of CyberDracula on 15.08.2017.
 * Full maintenance of plugin since 09.2020 (September) by Charlie Powell
 * This file no longer contains any work of previous contributors as of version 3.0
 */

function create_eeprom_observables(params) {
  var result = {};

  params.forEach(function (param) {
    result[param] = ko.observable();
  });

  result["visible"] = ko.computed(function () {
    for (let param in result) {
      if (param === "visible") {
        continue;
      }
      if (result[param]() !== null) {
        return true;
      }
    }
    return false;
  });
  return result;
}

$(function () {
  function EEPROMMarlinViewModel(parameters) {
    var self = this;

    self.printerState = parameters[0];
    self.settingsViewModel = parameters[1];
    self.loginState = parameters[2];
    self.access = parameters[3];

    self.eeprom = (function () {
      var eeprom = {};

      eeprom.advanced = create_eeprom_observables([
        "B",
        "E",
        "J",
        "S",
        "T",
        "X",
        "Y",
        "Z",
      ]);

      eeprom.autolevel = create_eeprom_observables(["S", "Z"]);

      eeprom.bed_pid = create_eeprom_observables(["D", "I", "P"]);

      eeprom.delta = create_eeprom_observables([
        "L",
        "R",
        "H",
        "S",
        "X",
        "Y",
        "Z",
        "A",
        "B",
        "C",
      ]);

      eeprom.endstop = create_eeprom_observables(["X", "Y", "Z"]);

      eeprom.feedrate = create_eeprom_observables(["X", "Y", "Z", "E"]);

      eeprom.filament = create_eeprom_observables(["D"]);

      eeprom.home_offset = create_eeprom_observables(["X", "Y", "Z"]);

      eeprom.hotend_pid = create_eeprom_observables(["P", "I", "D"]);

      eeprom.linear = create_eeprom_observables(["K"]);

      eeprom.material1 = create_eeprom_observables(["B", "F", "H"]);

      eeprom.material2 = create_eeprom_observables(["B", "F", "H"]);

      eeprom.max_acceleration = create_eeprom_observables(["E", "X", "Y", "Z"]);

      eeprom.print_acceleration = create_eeprom_observables(["P", "R", "T"]);

      eeprom.probe_offset = create_eeprom_observables(["X", "Y", "Z"]);

      eeprom.steps = create_eeprom_observables(["E", "X", "Y", "Z"]);

      eeprom.filament_change = create_eeprom_observables(["L", "U"]);

      eeprom.filament_runout = create_eeprom_observables(["D", "H", "S"]);

      eeprom.tmc_current = create_eeprom_observables(["E", "X", "Y", "Z"]);

      eeprom.tmc_hybrid = create_eeprom_observables(["E", "X", "Y", "Z"]);

      return eeprom;
    })();

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
        self.printerState.isReady() &&
        self.loginState.hasPermission(
          self.access.permissions.PLUGIN_EEPROM_MARLIN_EDIT
        )
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

    self.enableLoad = ko.pureComputed(function () {
      return (
        self.loginState.hasPermission(
          self.access.permissions.PLUGIN_EEPROM_MARLIN_READ
        ) && self.enable_buttons()
      );
    });

    self.enableSave = ko.pureComputed(function () {
      return (
        self.loginState.hasPermission(
          self.access.permissions.PLUGIN_EEPROM_MARLIN_EDIT
        ) && self.enable_buttons()
      );
    });

    self.enableReset = ko.pureComputed(function () {
      return (
        self.loginState.hasPermission(
          self.access.permissions.PLUGIN_EEPROM_MARLIN_RESET
        ) && self.enable_buttons()
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
      if (self.settingsViewModel.settings.plugins.eeprom_marlin.custom_name()) {
        // Trigger modal with custom name
        $("#eepromBackupNameModal").modal("show");
      } else {
        self.create_backup();
      }
    };

    $("#eepromBackupNameModal").on("shown", function () {
      $("#eepromBackupNameInput").focus();
    });

    self.create_backup = function () {
      $("#eepromBackupNameModal").modal("hide");

      var payload = {};
      if (self.settingsViewModel.settings.plugins.eeprom_marlin.custom_name()) {
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
            OctoPrint.simpleApiGet("eeprom_marlin").done(function (response) {
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

    self.onBackupUpload = function (data, event) {
      self.backup_upload_name(event.target.files[0].name);
    };

    self.restore_from_upload = function () {
      var fileInput = document.getElementById(
        "plugin_eeprom_marlin_backup_upload"
      );
      var files = fileInput.files;

      if (!fileInput.files.length) {
        // No files selected, no backup for you
        return;
      }

      var file = files.item(0);

      var fr = new FileReader();
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
          self.backup_upload_name("");
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
        self.eeprom_from_json(data.data);
        self.info_from_json(data.data);
        self.loading(false);
      }
    };

    self.onAllBound = self.onEventConnected = function () {
      if (
        self.loginState.hasPermission(
          self.access.permissions.PLUGIN_EEPROM_MARLIN_READ
        )
      ) {
        self.loading(true);
        OctoPrint.simpleApiGet("eeprom_marlin").done(function (response) {
          self.eeprom_from_json(response);
          self.info_from_json(response);
          self.backups_from_response(response.backups);
          self.loading(false);
          self.initialLoad(false);
        });
      }
    };

    // Utilities
    function capitaliseWords(str) {
      return str.replace(/\w\S*/g, function (txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
      });
    }
  }

  OCTOPRINT_VIEWMODELS.push({
    construct: EEPROMMarlinViewModel,
    dependencies: [
      "printerStateViewModel",
      "settingsViewModel",
      "loginStateViewModel",
      "accessViewModel",
    ],
    elements: ["#tab_plugin_eeprom_marlin"],
  });
});
