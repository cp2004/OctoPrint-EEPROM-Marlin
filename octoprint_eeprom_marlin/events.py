# -*- coding: utf-8 -*-
"""
OctoPrint event handling, in a module
"""
from octoprint.events import Events


class EventHandler:
    def __init__(self, plugin):
        self._logger = plugin._logger
        self._printer = plugin._printer
        self._settings = plugin._settings
        self.plugin = plugin

        self.event_to_react_to = {Events.CONNECTED: self.connected}

    def on_event(self, event, payload):
        if event in self.event_to_react_to:
            self.event_to_react_to[event](payload)

    def connected(self, payload):
        # No longer required, TODO remove this
        pass
