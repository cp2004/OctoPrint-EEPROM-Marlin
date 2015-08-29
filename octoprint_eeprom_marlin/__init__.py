# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import octoprint.server

class Eeprom_marlinPlugin(octoprint.plugin.AssetPlugin,
                            octoprint.plugin.TemplatePlugin):
    def get_assets(self):
        return dict(
            js=["js/eeprom_marlin.js"]
        )

    def get_template_configs(self):
        return [
            dict(type="settings", template="eeprom_marlin_settings.jinja2", custom_bindings=True)
        ]

    def get_update_information(self):
        return dict(
            systemcommandeditor=dict(
                displayName="EEPROM Marlin Editor Plugin",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="amsbr",
                repo="OctoPrint-EEPROM-Marlin",
                current=self._plugin_version,

                # update method: pip
                pip="https://github.com/amsbr/OctoPrint-EEPROM-Marlin/archive/{target_version}.zip"
            )
        )

__plugin_name__ = "EEPROM Marlin Editor Plugin"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = Eeprom_marlinPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
