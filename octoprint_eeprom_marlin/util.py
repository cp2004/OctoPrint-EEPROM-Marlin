# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import time


def build_backup_name():
    return "eeprom_backup-{}".format(time.strftime("%Y%m%d-%H%M%S"))
