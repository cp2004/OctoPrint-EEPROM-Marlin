# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = (
    "Copyright (C) 2020 Charlie Powell - Released under terms of the AGPLv3 License"
)
# Originally by Anderson Silva, development taken over by Charlie Powell in September 2020
# Vast majority of the work here is by Charlie Powell, for full details see the git history.
from copy import deepcopy

import octoprint.plugin

from octoprint_eeprom_marlin import _version, api, data, parser, settings
from octoprint_eeprom_marlin.events import EventHandler

__version__ = _version.get_versions()["version"]
del _version


class EEPROMMarlinPlugin(
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.WizardPlugin,
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.SimpleApiPlugin,
    octoprint.plugin.EventHandlerPlugin,
):
    # Data models
    _firmware_info = None
    _eeprom_data = None
    _changed_data = None

    # Useful classes
    _parser = None
    _api = None
    _event_reactor = None

    # Flags
    collecting_eeprom = False

    def initialize(self):
        # Initialise is called when all injections are complete
        # Means we can add our own things that depend on previous injected properties

        # Data models
        self._firmware_info = data.FirmwareInfo()
        self._eeprom_data = data.EEPROMData()

        # Useful classes
        self._parser = parser.Parser(self._logger)
        self._api = api.API(self)
        self._event_reactor = EventHandler(self)

        # Flags
        self.collecting_eeprom = False

    # Registering UI components
    def get_assets(self):
        return {
            "js": ["js/eeprom_marlin.js"],
            "css": ["css/fontawesome5_stripped.css", "css/eeprom_marlin.css"],
        }

    def is_wizard_required(self):
        return False

    def get_template_configs(self):
        return [
            {
                "type": "tab",
                "template": "eeprom_marlin_tab_old.jinja2",
                "div": "tab_plugin_eeprom_marlin_old",
                "custom_bindings": True,
            },
            {
                "type": "tab",
                "name": "EEPROM Editor",
                "template": "eeprom_marlin_tab.jinja2",
                "custom_bindings": True,
            },
        ]

    def get_template_vars(self):
        return {"version": self._plugin_version}

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

    # Event handling
    def on_event(self, event, payload):
        self._event_reactor.on_event(event, payload)

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
            # Connected and need to send M503
            command = "M503" if self._settings.get_boolean(["use_m503"]) else "M501"
            self._printer.commands(command)
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
        self._logger.debug(cmd)
        if cmd == "M501" or cmd == "M503":
            self._logger.info("M501/3 detected")
            self.collecting_eeprom = True

    def comm_protocol_gcode_received(self, comm, line, *args, **kwargs):
        # https://docs.octoprint.org/en/master/plugins/hooks.html#octoprint-comm-protocol-gcode-received
        if self.collecting_eeprom:
            if "ok" in line.lower():
                # Send the new data to the UI to be reloaded
                self.send_message(
                    "load",
                    {
                        "eeprom": self._eeprom_data.to_dict(),
                        "info": self._firmware_info.to_dict(),
                    },
                )
                self.collecting_eeprom = False
            else:
                parsed = self._parser.parse_eeprom_data(line)
                if parsed:
                    self._eeprom_data.from_dict(parsed, ui=False)

        return line

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
    }
