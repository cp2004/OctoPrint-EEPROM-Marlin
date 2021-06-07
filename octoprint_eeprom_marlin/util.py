# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = (
    "Copyright (C) 2020 Charlie Powell - Released under terms of the AGPLv3 License"
)
import time

from octoprint_eeprom_marlin.data import ALL_DATA_STRUCTURE as DATA


def build_backup_name():
    return "eeprom_backup-{}".format(time.strftime("%Y%m%d-%H%M%S"))


def construct_command(data, name):
    command = data["command"]
    for param, value in data["params"].items():
        # Check that the value exists, avoid M205 [...] JNone
        if value is None:
            continue

        # Check the command type, and map boolean back to 0/1
        if DATA[name]["params"][param]["type"] == "bool":
            value = "1" if value is True else "0"
        else:
            value = (
                str(value) if command != "M145" and param != "S" else str(int(value))
            )

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
    # OctoPrint>=1.6.0
    from octoprint.util.text import sanitize
except ImportError:
    # OctoPrint<=1.5.x
    # Use back-ported version
    import re

    # noinspection PyPackageRequirements
    from emoji import demojize
    from octoprint.util import to_unicode

    try:
        # OctoPrint>=1.4.1
        from octoprint.vendor.awesome_slugify import Slugify
    except ImportError:
        # OctoPrint<=1.4.0
        from slugify import Slugify  # noqa

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
            demoji: whether to also convert emoji to text
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
