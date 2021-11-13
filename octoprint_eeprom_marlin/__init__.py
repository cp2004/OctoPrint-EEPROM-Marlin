# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = (
    "Copyright (C) 2020 Charlie Powell - Released under terms of the AGPLv3 License"
)
import json

# Originally by Anderson Silva, development taken over by Charlie Powell in September 2020
# Vast majority of the work here is by Charlie Powell, for full details see the git history.
from copy import deepcopy

import flask
import octoprint.plugin
from octoprint.access import ADMIN_GROUP, READONLY_GROUP, USER_GROUP
from octoprint.access.permissions import Permissions
from octoprint.util.version import is_octoprint_compatible

from octoprint_eeprom_marlin import (
    _version,
    api,
    backup,
    data,
    parser,
    settings,
    sponsors_contributors,
)

__version__ = _version.get_versions()["version"]
del _version


class EEPROMMarlinPlugin(
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.WizardPlugin,
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.SimpleApiPlugin,
    octoprint.plugin.BlueprintPlugin,
):
    # Data models
    _firmware_info = None
    _eeprom_data = None
    _changed_data = None

    # Useful classes
    _backup_handler = None
    _parser = None
    _api = None
    _event_reactor = None

    # Flags
    collecting_eeprom = False
    collecting_stats = False

    def initialize(self):
        # Initialise is called when all injections are complete
        # Means we can add our own things that depend on previous injected properties
        self._logger.debug("Starting up EEPROM editor, intialising modules...")

        # Data models
        self._firmware_info = data.FirmwareInfo()
        self._firmware_stats = data.FirmwareStats()
        self._eeprom_data = data.EEPROMData(self)

        # Useful classes - watch the inheritance order:
        # API requires backup handler
        self._backup_handler = backup.BackupHandler(self)
        self._parser = parser.Parser(self._logger)
        self._api = api.API(self)

        self._logger.info("All EEPROM editor modules loaded")

        # Flags
        self.collecting_eeprom = False

    # Registering UI components
    def get_assets(self):
        # OctoPrint 1.5.0+ bundles FontAwesome 5, earlier versions do not
        css_assets = ["css/eeprom_marlin.css"]
        if is_octoprint_compatible("<1.5.0"):
            css_assets += ["css/fontawesome5_stripped.css"]

        return {"js": ["js/eeprom_marlin.js"], "css": css_assets}

    def is_wizard_required(self):
        return False

    def get_template_configs(self):
        return [
            {
                "type": "tab",
                "name": "EEPROM Editor",
                "template": "eeprom_marlin_tab.jinja2",
                "custom_bindings": True,
            },
            {
                "type": "settings",
                "name": "Marlin EEPROM Editor",
                "template": "eeprom_marlin_settings.jinja2",
                "custom_bindings": False,
            },
        ]

    def get_template_vars(self):
        return {
            "version": self._plugin_version,
            "DATA_STRUCTURE": data.ALL_DATA_STRUCTURE,
            "SPONSORS": sponsors_contributors.export_sponsors(),
            "CONTRIBUTORS": sponsors_contributors.export_contributors(),
        }

    # Settings handling - see settings submodule
    def get_settings_defaults(self):
        return settings.defaults

    # API handling
    def get_api_commands(self):
        return self._api.get_api_commands()

    def on_api_command(self, command, data):
        return self._api.on_api_command(command, data)

    def on_api_get(self, request):
        return self._api.on_api_get(request)

    # BluePrint handling
    @octoprint.plugin.BlueprintPlugin.route("/download/<name>")
    @Permissions.PLUGIN_EEPROM_MARLIN_READ.require(403)
    def download_backup(self, name):
        try:
            backup_data = self._backup_handler.read_backup(name)
        except backup.BackupMissingError:
            flask.abort(404)
            return

        return flask.Response(
            json.dumps(backup_data),
            mimetype="text/plain",
            headers={
                "Content-Disposition": 'attachment; filename="{}.json"'.format(name)
            },
        )

    # Websocket communication
    def send_message(self, type, data):
        payload = {"type": type, "data": data}
        self._plugin_manager.send_plugin_message("eeprom_marlin", payload)

    # Hook handlers
    def comm_protocol_firmware_info(self, comm, name, fw_data, *args, **kwargs):
        # https://docs.octoprint.org/en/master/plugins/hooks.html#octoprint-comm-protocol-firmware-info
        old_is_marlin = deepcopy(self._firmware_info.is_marlin)
        self._firmware_info.is_marlin = self._parser.is_marlin(name)
        if not old_is_marlin and self._firmware_info.is_marlin:
            # Connected and need to send M503 (& optionally M78)
            commands = ["M503" if self._settings.get(["use_m503"]) else "M501"]
            if self._settings.get_boolean(["m78"]):
                commands += ["M78"]
            self._printer.commands(commands)
        self._firmware_info.name = name
        self._firmware_info.additional_info_from_dict(fw_data)

    def comm_protocol_firmware_cap(
        self, comm, cap, enabled, already_defined, *args, **kwargs
    ):
        # https://docs.octoprint.org/en/master/plugins/hooks.html#firmware_capability_hook
        self._firmware_info.add_capabilities(already_defined)

    def comm_protocol_gcode_sending(
        self,
        comm,
        phase,
        cmd,
        cmd_type,
        gcode,
        subcode=None,
        tags=None,
        *args,
        **kwargs
    ):
        # https://docs.octoprint.org/en/master/plugins/hooks.html#protocol_gcodephase_hook
        if cmd == "M501" or cmd == "M503":
            self._logger.info("{} detected, collecting data".format(cmd))
            self.collecting_eeprom = True

        if cmd == "M78":
            self._logger.info("M87 detected, collecting stats")
            self.collecting_stats = True

    def comm_protocol_gcode_received(self, comm, line, *args, **kwargs):
        # https://docs.octoprint.org/en/master/plugins/hooks.html#octoprint-comm-protocol-gcode-received
        if self.collecting_eeprom or self.collecting_stats:
            if "ok" in line.lower():
                # Send the new data to the UI to be reloaded
                self._logger.info("Finished data collection, updating UI")
                self.send_message(
                    "load",
                    {
                        "eeprom": self._eeprom_data.to_dict(),
                        "info": self._firmware_info.to_dict(),
                        "stats": self._firmware_stats.get_stats(),
                    },
                )
                self.collecting_eeprom = False
                self.collecting_stats = False

            elif "printer locked" in line.lower():
                self._logger.info("Printer locked, aborting data collection")
                self.send_message("locked", {})
                self.collecting_eeprom = False
                self.collecting_stats = False

        if self.collecting_eeprom:
            parsed = self._parser.parse_eeprom_data(line)
            if parsed:
                self._eeprom_data.from_dict(parsed, ui=False)
        elif self.collecting_stats:
            stats = self._parser.parse_stats_line(line)
            if stats:
                self._firmware_stats.update_stats(stats)

        return line

    def comm_protocol_atcommand_sending(
        self, comm, phase, cmd, params, tags=None, *args, **kwargs
    ):
        if cmd.upper() == "EEPROM_DEBUG":
            # Trigger data collection manually using @EEPROM_DEBUG, for sending test files at the parser
            # Useful for virtual printer testing, where the responses are not implemented.
            self.collecting_eeprom = True

        if cmd.upper() == "EEPROM_STATS_DEBUG":
            # Trigger stats data collection manually using @EEPROM_STATS_DEBUG, for sending test files at the parser
            # Useful for virtual printer testing, where the responses are not implemented.
            self.collecting_stats = True

    def get_additional_permissions(self, *args, **kwargs):
        return [
            {
                "key": "READ",
                "name": "Read EEPROM",
                "description": "Can read EEPROM data",
                "roles": ["read"],
                "dangerous": False,
                "default_groups": [ADMIN_GROUP, USER_GROUP, READONLY_GROUP],
            },
            {
                "key": "EDIT",
                "name": "Edit EEPROM",
                "description": "Can edit EEPROM data and save it to the printer",
                "roles": ["edit"],
                "dangerous": False,
                "default_groups": [ADMIN_GROUP, USER_GROUP],
            },
            {
                "key": "RESET",
                "name": "Reset EEPROM",
                "description": "Can reset the firmware to factory defaults",
                "roles": ["reset"],
                "dangerous": True,
                "default_groups": [ADMIN_GROUP],
            },
        ]

    # Update hook
    def get_update_information(self):
        # https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html#sec-bundledplugins-softwareupdate-hooks-check-config
        return {
            "eeprom_marlin": {
                "displayName": "Marlin EEPROM Editor",
                "displayVersion": self._plugin_version,
                # version check: github repository
                "type": "github_release",
                "user": "cp2004",
                "repo": "OctoPrint-EEPROM-Marlin",
                "current": self._plugin_version,
                "stable_branch": {
                    "name": "Stable",
                    "branch": "master",
                    "comittish": ["master"],
                },
                "prerelease_branches": [
                    {
                        "name": "Release Candidate",
                        "branch": "pre-release",
                        "comittish": ["pre-release", "master"],
                    }
                ],
                # update method: pip
                "pip": "https://github.com/cp2004/OctoPrint-EEPROM-Marlin/archive/{target_version}.zip",
            }
        }


__plugin_name__ = "Marlin EEPROM Editor"
__plugin_description__ = """
    Makes it possible to change the EEPROM values of Marlin Firmware through OctoPrint.
    Plugin previously maintained by Anderson Silva, currently Charlie Powell.
    """
__plugin_author__ = "Charlie Powell"
__plugin_license__ = "AGPLv3"
__plugin_url__ = "https://github.com/cp2004/OctoPrint-EEPROM-Marlin"
__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_version__ = __version__


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = EEPROMMarlinPlugin()
    plugin = __plugin_implementation__

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": plugin.get_update_information,
        "octoprint.comm.protocol.firmware.info": plugin.comm_protocol_firmware_info,
        "octoprint.comm.protocol.firmware.capabilities": plugin.comm_protocol_firmware_cap,
        "octoprint.comm.protocol.gcode.received": plugin.comm_protocol_gcode_received,
        "octoprint.comm.protocol.gcode.sending": plugin.comm_protocol_gcode_sending,
        "octoprint.comm.protocol.atcommand.sending": plugin.comm_protocol_atcommand_sending,
        "octoprint.access.permissions": plugin.get_additional_permissions,
    }
