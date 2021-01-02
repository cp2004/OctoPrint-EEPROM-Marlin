# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import time


def build_backup_name():
    return "eeprom_backup-{}".format(time.strftime("%Y%m%d-%H%M%S"))


def construct_command(data):
    command = data["command"]
    for param, value in data["params"].items():
        # Check that the value exists, avoid M205 [...] JNone
        if value is None:
            continue
        value = str(value) if command != "M145" and param != "S" else str(int(value))
        command = command + " " + param + value
    return command


def backup_json_to_list(eeprom_data):
    eeprom_list = []
    for key in eeprom_data.keys():
        eeprom_list.append(
            {
                "name": key,
                "command": eeprom_data[key]["command"],
                "params": eeprom_data[key]["params"],
            }
        )

    return eeprom_list


try:
    # This is available in OP 1.6.0+
    # TODO decide when to stop supporting 1.5.x and below
    from octoprint.util.text import sanitize
except ImportError:
    # We are below this version, use backported one instead
    import re

    from emoji import demojize
    from octoprint.util import to_unicode
    from octoprint.vendor.awesome_slugify import Slugify

    _UNICODE_VARIATIONS = re.compile("[\uFE00-\uFE0F]", re.U)
    _SLUGIFIES = {}

    def sanitize(text, safe_chars="-_.", demoji=True):
        """
        Sanitizes text by running it through slugify and optionally emoji translating.
        Examples:
        >>> sanitize("Hello World!") # doctest: +ALLOW_UNICODE
        'Hello-World'
        >>> sanitize("Hello World!", safe_chars="-_. ") # doctest: +ALLOW_UNICODE
        'Hello World'
        >>> sanitize("\u2764") # doctest: +ALLOW_UNICODE
        'red_heart'
        >>> sanitize("\u2764\ufe00") # doctest: +ALLOW_UNICODE
        'red_heart'
        >>> sanitize("\u2764", demoji=False) # doctest: +ALLOW_UNICODE
        ''
        Args:
            text: the text to sanitize
            safe_chars: characters to consider safe and to keep after sanitization
            emoji: whether to also convert emoji to text
        Returns: the sanitized text
        """
        slugify = _SLUGIFIES.get(safe_chars)
        if slugify is None:
            slugify = Slugify()
            slugify.safe_chars = safe_chars
            _SLUGIFIES[safe_chars] = slugify

        text = to_unicode(text)
        if demoji:
            text = remove_unicode_variations(text)
            text = demojize(text, delimiters=("", ""))
        return slugify(text)

    def remove_unicode_variations(text):
        return _UNICODE_VARIATIONS.sub("", text)
