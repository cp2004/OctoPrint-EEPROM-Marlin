/**
 * Plugin was Created by Salandora on 27.07.2015, Modified by Anderson Silva on 20.08.2017, Contribution of CyberDracula on 15.08.2017.
 * Full maintenance of plugin since 09.2020 (September) by Charlie Powell
 * This file no longer contains any work of previous contributors as of version 3.0
 */

function create_eeprom_observables(params, switches) {
  var result = {};

  params.forEach(function (param, switches) {
    result[param] = ko.observable();
  });

  if (switches) {
    switches.forEach(function (param) {
      result[param] = ko.observableArray();
    });
  }

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

      eeprom.feedrate = create_eeprom_observables(["X", "Y", "Z", "E"], ["T"]);

      eeprom.filament = create_eeprom_observables(["D"], ["T"]);

      eeprom.home_offset = create_eeprom_observables(["X", "Y", "Z"]);

      eeprom.hotend_pid = create_eeprom_observables(["P", "I", "D"], ["E"]);

      eeprom.hotend_mpc = create_eeprom_observables(
        ["A", "C", "F", "H", "P", "R"],
        ["E"]
      );

      eeprom.linear = create_eeprom_observables(["K"]);

      eeprom.material = create_eeprom_observables(["B", "F", "H"], ["S"]);

      eeprom.max_acceleration = create_eeprom_observables(
        ["E", "X", "Y", "Z"],
        ["T"]
      );

      eeprom.print_acceleration = create_eeprom_observables(["P", "R", "T"]);

      eeprom.probe_offset = create_eeprom_observables(["X", "Y", "Z"]);

      eeprom.steps = create_eeprom_observables(["E", "X", "Y", "Z"], ["T"]);

      eeprom.filament_change = create_eeprom_observables(["L", "U"]);

      eeprom.filament_runout = create_eeprom_observables(["D", "H", "S"]);

      eeprom.tmc_current = create_eeprom_observables(
        ["E", "X", "Y", "Z"],
        ["I", "T"]
      );

      eeprom.tmc_hybrid = create_eeprom_observables(
        ["E", "X", "Y", "Z"],
        ["I", "T"]
      );

      eeprom.input_shaping = create_eeprom_observables(["D", "F"]);

      return eeprom;
    })();

    self.eeprom_from_json = function (data) {
      // loops through response and assigns values to observables
      for (let key in data.eeprom) {
        let value = data.eeprom[key];
        // Store switched params to deal with after the loop
        const switched = [];
        for (let param in value.params) {
          if (
            typeof value.params[param] === "object" &&
            value.params[param] !== null
          ) {
            // Save for later
            switched.push(param);
          } else {
            try {
              self.eeprom[key][param](value.params[param]);
            } catch {
              console.log("unable to parse response - " + key + ": " + param);
            }
          }
        }
        if (switched.length > 0) {
          // Empty any switched arrays
          switched.forEach((sw) => {
            try {
              self.eeprom[key][sw.charAt(0)]([]);
            } catch {
              console.log(
                "unable to empty switched array for " +
                  key +
                  " (" +
                  sw.charAt(0) +
                  ")"
              );
            }
          });
          // Now fill them back up
          switched.forEach((sw) => {
            try {
              const result = ko.mapping.fromJS(value.params[sw]);
              result["key"] = sw;
              self.eeprom[key][sw.charAt(0)].push(result);
            } catch {
              console.log(
                "unable to fill switched array for " + key + " (" + sw + ")"
              );
            }
          });
        }
      }
      self.unsaved(false);
    };

    self.eeprom_to_json = function () {
      // loops through eeprom data, to create a JSON object to POST
      const eeprom = [];
      for (const key in self.eeprom) {
        const data = { name: key, params: {} };
        const value = self.eeprom[key];
        for (const param in value) {
          if (param === "visible") continue;

          if (typeof value[param]() === "object" && value[param]() !== null) {
            // We have a switched param
            value[param]().forEach((sw) => {
              data.params[sw.key] = ko.mapping.toJS(sw);
            });
          } else {
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

      const capabilities = stableSort(
        Object.keys(data.info.capabilities),
        ascendingComparator
      );
      self.info.capabilities(
        capabilities.map((capability) => ({
          cap: capitaliseWords(capability.replace(/_/gi, " ")),
          val: data.info.capabilities[capability],
          link: link_for_cap(capability),
        }))
      );

      self.info.is_marlin(data.info.is_marlin);
      self.info.name(data.info.name);
      self.printer_locked(data.info.locked);
    };

    self.stats = (function () {
      var stats = {};

      stats.prints = ko.observable("");
      stats.finished = ko.observable("");
      stats.failed = ko.observable("");
      stats.total_time = ko.observable("");
      stats.longest = ko.observable("");
      stats.filament = ko.observable("");

      return stats;
    })();

    self.stats_from_json = function (data) {
      self.stats.prints(data.prints);
      self.stats.finished(data.finished);
      self.stats.failed(data.failed);
      self.stats.total_time(data.total_time);
      self.stats.longest(data.longest);
      self.stats.filament(data.filament);
    };

    self.backups = ko.observableArray([]);
    self.backup_upload_name = ko.observable();

    // State bindings
    self.loading = ko.observable(false);
    self.initialLoad = ko.observable(true);
    self.saving = ko.observable(false);
    self.unsaved = ko.observable(false);

    self.printer_locked = ko.observable(false);

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
        (self.info.is_marlin() || self.printer_locked()) && // Allow refresh button when locked
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
        self.stats_from_json(data.data.stats);
        self.loading(false);
        self.printer_locked(false);
      }
      if (data.type === "locked") {
        self.loading(false);
        self.printer_locked(true);
      }
      if (data.type === "unlocked") {
        self.loading(false);
        self.printer_locked(false);
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
          self.stats_from_json(response.stats);
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

function ascendingComparator(a, b) {
  if (b > a) {
    return -1;
  }
  if (b < a) {
    return 0;
  }
  return 0;
}

function stableSort(array, comparator) {
  const stabilizedThis = array.map((el, index) => [el, index]);
  stabilizedThis.sort((a, b) => {
    const order = comparator(a[0], b[0]);
    if (order !== 0) return order;
    return a[1] - b[1];
  });
  return stabilizedThis.map((el) => el[0]);
}

const KNOWN_CAPABILITIES = {
  /*
   * These are known capabililties, retrieved from the Marlin source (11/21) and some docs links found.
   */
  PAREN_COMMENTS:
    "https://marlinfw.org/docs/configuration/configuration.html#cnc-g-code-options",
  // "QUOTED_STRINGS": "",
  SERIAL_XON_XOFF:
    "https://marlinfw.org/docs/configuration/configuration.html#host-receive-buffer",
  BINARY_FILE_TRANSFER:
    "https://marlinfw.org/docs/configuration/configuration.html#binary-file-transfer",
  EEPROM: "https://marlinfw.org/docs/configuration/configuration.html#eeprom",
  VOLUMETRIC:
    "https://marlinfw.org/docs/configuration/configuration.html#volumetric-mode-default",
  AUTOREPORT_POS: "https://marlinfw.org/docs/gcode/M154.html",
  AUTOREPORT_TEMP:
    "https://marlinfw.org/docs/configuration/configuration.html#temperature-auto-report",
  // "PROGRESS": "",  // Seems to have no options associated
  PRINT_JOB: "https://marlinfw.org/docs/gcode/M075.html",
  AUTOLEVEL: "https://marlinfw.org/docs/features/auto_bed_leveling.html",
  RUNOUT:
    "https://marlinfw.org/docs/configuration/configuration.html#filament-runout-sensor",
  Z_PROBE: "https://marlinfw.org/docs/features/auto_bed_leveling.html",
  LEVELING_DATA: "https://marlinfw.org/docs/gcode/M420.html",
  BUILD_PERCENT:
    "https://marlinfw.org/docs/configuration/configuration.html#set-print-progress",
  SOFTWARE_POWER:
    "https://marlinfw.org/docs/configuration/configuration.html#power-supply",
  TOGGLE_LIGHTS:
    "https://marlinfw.org/docs/configuration/configuration.html#case-light",
  CASE_LIGHT_BRIGHTNESS:
    "https://marlinfw.org/docs/configuration/configuration.html#case-light",
  EMERGENCY_PARSER:
    "https://marlinfw.org/docs/configuration/configuration.html#emergency-parser",
  HOST_ACTION_COMMANDS:
    "https://marlinfw.org/docs/configuration/configuration.html#host-action-commands",
  "PROMPT-SUPPORT":
    "https://marlinfw.org/docs/configuration/configuration.html#host-action-commands",
  SDCARD: "https://marlinfw.org/docs/configuration/configuration.html#sd-card",
  REPEAT: "https://marlinfw.org/docs/gcode/M808.html",
  SD_WRITE:
    "https://marlinfw.org/docs/configuration/configuration.html#sd-card-support",
  AUTOREPORT_SD_STATUS:
    "https://marlinfw.org/docs/configuration/configuration.html#auto-report-sd-status",
  LONG_FILENAME:
    "https://marlinfw.org/docs/configuration/configuration.html#long-filenames",
  THERMAL_PROTECTION:
    "https://marlinfw.org/docs/configuration/configuration.html#safety",
  MOTION_MODES:
    "https://marlinfw.org/docs/configuration/configuration.html#cnc-g-code-options",
  ARCS: "https://marlinfw.org/docs/configuration/configuration.html#g2/g3-arc-support",
  BABYSTEPPING:
    "https://marlinfw.org/docs/configuration/configuration.html#babystepping",
  CHAMBER_TEMPERATURE:
    "https://marlinfw.org/docs/configuration/configuration.html#heated-chamber",
  COOLER_TEMPERATURE: "https://marlinfw.org/docs/gcode/M143.html",
  // "MEATPACK": "",
};

function link_for_cap(cap) {
  if (KNOWN_CAPABILITIES[cap]) {
    return KNOWN_CAPABILITIES[cap];
  }
  return "";
}
