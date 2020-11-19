# -*- coding: utf-8 -*-
from __future__ import absolute_import

__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = (
    "Copyright (C) 2020 Charlie Powell - Released under terms of the AGPLv3 License"
)
# Originally by Anderson Silva, development taken over by Charlie Powell in September 2020

import octoprint.plugin

from octoprint_eeprom_marlin import _version, settings

__version__ = _version.get_versions()["version"]
del _version


class EEPROMMarlinPlugin(
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.WizardPlugin,
    octoprint.plugin.SettingsPlugin,
):
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
                "template": "eeprom_marlin_tab.jinja2",
                "custom_bindings": True,
            }
        ]

    def get_settings_defaults(self):
        return settings.defaults

    def get_template_vars(self):
        return {"version": self._plugin_version}

    def get_update_information(self):
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

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
