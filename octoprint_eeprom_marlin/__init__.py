# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin


class EEPROM_MarlinPlugin(octoprint.plugin.AssetPlugin,
                          octoprint.plugin.TemplatePlugin):
    def get_assets(self):
        return dict(
            js=["js/eeprom_marlin.js"]
        )

    def get_template_configs(self):
        return [
            dict(type="tab", template="eeprom_marlin_tab.jinja2", custom_bindings=True)
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
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = EEPROM_MarlinPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
