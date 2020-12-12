# -*- coding: utf-8 -*-
"""
Handles backing up, saving, loading, restoring and more related to the backups
"""
import io
import json
import os
import time

from octoprint.util import to_unicode

METADATA_FILENAME = "backup_metadata.json"
METDATA_VERSION = 1  # Incremented when the schema has to be changed
BACKUPS_PATH = "backups"  # eg. ~/.octoprint/plugins/eeprom_marlin/backups
BACKUP_VERSION = 1  # Incremented when the schema has to be changed

# speaking of schemas, here's what they are looking like
# METADATA = \
#     {
#         "version": METDATA_VERSION,
#         "backups": [
#             {
#                 "name": backup_filename,
#                 "time": backup_time,
#             }
#         ]
#     }
# BACKUP = \
#     {
#         "version": BACKUP_VERSION,
#         "time": backup_time,
#         "name": backup_filename,
#         "data" response from eeprom data class (json)
#     }


class BackupHandler:
    """
    Class encapsulating backup handling
    Holds metadata on the names of backups,
    creating backups, reading backups, validating and more

    """

    def __init__(self, plugin):
        self.plugin = plugin
        self._data_folder = self.plugin.get_plugin_data_folder()
        self._settings = plugin._settings
        self._logger = plugin._logger
        self._metadata_file_path = os.path.join(self._data_folder, METADATA_FILENAME)
        self.metadata = None

        # Make sure we have the metadata available
        try:
            # Try read from disk
            self.get_backups(quick=False)
        except MetadataMissingError as e:
            self._logger.exception(e)
            self._logger.warning("Metadata was missing, re-creating")
            self.get_backups(scan=True)
        except MetadataInvalidError as e:
            self._logger.exception(e)
            self._logger.warning("Metadata was invalid, re-creating")
            self.get_backups(scan=True)
        except Exception as e:
            self._logger.error("Unknown error reading metadata")
            self._logger.exception(e)
            raise

    def get_backups(self, quick=True, scan=False):
        """
        Find all backups registered in the system
        if reload is true, scans folder & regenerates metadata - this could be a performance hit
        otherwise checks metadata file on disk, doesn't scan folder
        :return: list: list of backup names
        """
        if quick and not scan and isinstance(self.metadata, MetaData):
            # Return what we already have in memory
            return self.metadata.backups

        if not scan:
            # Read metadata from disk, don't scan
            if not os.path.exists(self._metadata_file_path):
                raise MetadataMissingError(
                    "Could not locate metadata file at {}".format(
                        self._metadata_file_path
                    )
                )

            with io.open(self._metadata_file_path, "rt") as metadata:
                data = json.load(metadata)
                if not self._validate_metadata(data):
                    raise MetadataInvalidError(
                        "Invalid metadata file at {}".format(self._metadata_file_path)
                    )
                else:
                    self.metadata = MetaData(
                        self._metadata_file_path, data, self._data_folder
                    )
            return self.metadata.backups

        else:
            # Performance intensive scanning of the folder & regenerating metadata
            backups = self._scan_backup_folder()
            meta = []
            for backup in backups:
                # This reads *every* backup to find it's time
                # So it is not ever going to be called, unless the metadata file goes missing
                backup_data = self.read_backup(backup)
                name = backup_data["name"]
                time = backup_data["time"]
                meta.append({"name": name, "time": time})

            self.metadata = MetaData(
                self._metadata_file_path,
                {"version": METDATA_VERSION, "backups": meta},
                self._data_folder,
            )
            return self.metadata.backups

    def create_backup(self, name, data, backup_time=None):
        """
        Creates a backup on the filesystem of data, with a name & time
        :param name: what to call the backup
        :param data: json data from the EEPROM
        :param backup_time: override the default time of 'now'
        :return: None
        """
        for backup in self.metadata.backups:
            if backup["name"] == name:
                raise BackupNameTakenError("Backup {} already exists!".format(name))

        if not backup_time:
            now = time.asctime(time.localtime())
        else:
            now = backup_time

        with io.open(self._get_backup_filename(name), "wt") as backup_file:
            backup_file.write(
                to_unicode(
                    json.dumps(
                        {
                            "name": name,
                            "time": now,
                            "version": BACKUP_VERSION,
                            "data": data,
                        }
                    )
                )
            )

        self.metadata.add_backup(name, now)

    def read_backup(self, name):
        """
        Read & return backup data
        Validation MUST be done downstream by the parser
        :param name: backup name
        :return: data: JSON data from the backup
        :raises BackupMissingError if backup couldn't be found.
        """
        if not os.path.exists(self._get_backup_filename(name)):
            raise BackupMissingError("Backup could not be loaded from {}".format(name))

        with io.open(self._get_backup_filename(name), "rt") as backup_file:
            data = json.load(backup_file)

        return data

    def _get_backup_filename(self, name):
        """
        Joins backup name to the intended storage location
        :param name:
        :return:
        """
        return os.path.join(self._data_folder, BACKUPS_PATH, "{}.json".format(name))

    def _validate_metadata(self, data):
        """
        Quick test that the metadata file looks like a metadata file
        :param data: contents of the file
        :return: bool: Whether the data looks valid (true) or not (false)
        """
        try:
            data["version"]
            backups = data["backups"]
            if isinstance(backups, list):
                return True
            else:
                return False
        except KeyError:
            return False

    def _validate_backup(self, name):
        """
        This does some basic checking that required items such as name, date & version exist
        :return: bool: if the backup is valid
        """
        data = self.read_backup(name)
        try:
            data["version"]
            data["time"]
            data["name"]
            data["data"]
            return True
        except KeyError:
            return False

    def _scan_backup_folder(self):
        """
        Looks for all files in the directory, and sees if they look valid
        :return:
        """
        files = []
        for (_path, _dirnames, filenames) in os.walk(
            os.path.join(self._data_folder, BACKUPS_PATH)
        ):
            valids = []
            for file in filenames:
                # TODO optimise performance here - this may make the backup be read twice
                name, _ext = os.path.splitext(file)
                if self._validate_backup(name):
                    valids.append(name)

            files.extend(valids)
            # Only walk one level
            break

        return files


class MetaData:
    def __init__(self, path, metadata, plugin_folder):
        self.path = path
        self.folder = plugin_folder
        self.version = metadata["version"]
        self.backups = metadata["backups"]
        self.save_metadata()

    def get_backup_time(self, name):
        """
        Grabs the time for a specifed backup
        :param name: backup filename
        :return: str: timestamp of backup
        """
        for backup in self.backups:
            if backup["name"] == name:
                return backup["time"]

    def get_backup_path(self, name):
        """
        Simple validation on a path in the metadata file
        raises BackupMissingError if it can't be found
        :param name: (str) name of backup
        :return: path
        """
        path = os.path.join(self.folder, name)
        if not os.path.exists(path):
            raise BackupMissingError("Backup not found at {}".format(path))
        else:
            return path

    def save_metadata(self):
        """
        Write metadata to disk
        :return: None
        """
        data = {"version": self.version, "backups": self.backups}
        with io.open(self.path, "wt", encoding="utf-8") as metadata_file:
            metadata_file.write(to_unicode(json.dumps(data)))

    def add_backup(self, name, time):
        """
        Append a backup to the metadata list & save it
        :param name: backup name
        :param time: backup time
        :return: None
        """
        data = {"name": name, "time": time}
        self.backups.append(data)
        self.save_metadata()


class MetadataMissingError(Exception):
    """Metadata file has gone missing"""

    pass


class MetadataInvalidError(Exception):
    """Metadata file seems invalid"""

    pass


class BackupMissingError(Exception):
    """Backup file has gone missing"""

    pass


class BackupInvalidError(Exception):
    """Backup file seems invalid"""

    pass


class BackupNameTakenError(Exception):
    """The backup name already exists!"""

    pass
