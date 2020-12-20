# -*- coding: utf-8 -*-
import time
import unittest

import mock

from octoprint_eeprom_marlin import backup

OPEN_SIGNATURE = "io.open"
MOCK_PLUGIN_DATAFOLDER = "/home/pi/.octoprint/data/eeprom_marlin"


class BackupTestCase(unittest.TestCase):
    def test_metadata_cls(self):
        time1 = time.asctime(time.localtime())
        time2 = time.asctime(time.localtime())

        mock_meta = {
            "version": backup.METDATA_VERSION,
            "backups": [
                {"name": "backup1", "time": time1},
                {"name": "backup2", "time": time2},
            ],
        }
        with mock.patch(OPEN_SIGNATURE, mock.mock_open(), create=True):
            metadata = backup.MetaData(
                MOCK_PLUGIN_DATAFOLDER + backup.METADATA_FILENAME,
                mock_meta,
                MOCK_PLUGIN_DATAFOLDER,
            )

        self.assertEqual(metadata.backups, mock_meta["backups"])
        self.assertEqual(metadata.version, mock_meta["version"])
