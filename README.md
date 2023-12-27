# ✏️ Marlin EEPROM Editor

The Marlin EEPROM editor provides an easy to use, feature-rich UI to edit your machine's configuration.

## ✨ Features

- Load and parse a wide range of EEPROM data out of the firmware
- Edit all the data in a user-friendly UI
- Save EEPROM changes on the printer with a minimal number of commands
- Storage of data on the OctoPrint server, so it can be viewed while printer is disconnected or printing.
- Backup feature:
  - Enabled saving configuration snapshots, restoring, downloading, uploading
- Displaying firmware info, including capability report & printer statistics
- Links to Marlin documentation to help you understand the settings

Be sure to [check out the screenshots](#screenshots) below for more details!

## 🔧 Setup

Install via the bundled [plugin manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html) or manually using this URL:

    https://github.com/cp2004/OctoPrint-EEPROM-Marlin/releases/latest/download/release.zip

## 🏗️ Firmware requirements

This plugin requires three things:

- `EEPROM_CHITCHAT` function - make sure you have `#define EEPROM_CHITCHAT` in the config
- The `M503` command enabled - do not uncomment disabling it, leave it as `//#define DISABLE_M503`
- Of course, EEPROM to be enabled 🙂

## 🎉 New in Marlin EEPROM Editor V3

A complete re-write of this plugin, now V3!

Featuring:

- Python processing & storage, eliminating performance issues in the UI.
- Storage of data on the OctoPrint server, so it can be viewed while the printer is disconnected or printing.
- Brand new UI, written from the ground up.
- All-new backup feature, allowing naming and storing of backups, so you can quickly swap between profiles and more.

## Screenshots

Firmware info overview
![Firmware Info](assets/firmware_info.png)

Configuration editor
![Configuration Editor](assets/config.png)

Backup feature
![Backup feature](assets/backup.png)

## Sponsors

- [@KenLucke](https://github.com/KenLucke)
- [@CmdrCody51](https://github.com/CmdrCody51)

As well as 2 others supporting me regularly through [GitHub Sponsors](https://github.com/sponsors/cp2004)!

## Supporting my efforts

![GitHub Sponsors](https://img.shields.io/github/sponsors/cp2004?style=for-the-badge&label=Sponsor!&color=red&link=https%3A%2F%2Fgithub.com%2Fsponsors%2Fcp2004)

I created this project in my spare time, and do my best to support the community with issues and help using it. If you have found this useful or enjoyed using it then please consider [supporting it's development! ❤️](https://github.com/sponsors/cp2004). You can sponsor monthly or one time, for any amount you choose.

## Check out my other plugins

You can see all of my published OctoPrint plugins [on the OctoPrint Plugin Repository!](https://plugins.octoprint.org/by_author/#charlie-powell) Or, if you're feeling nosy and want to see what else I'm working on, check out my [GitHub profile](https://github.com/cp2004).
## ✏️ 🔧
