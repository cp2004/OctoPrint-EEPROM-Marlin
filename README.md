# Marlin EEPROM Editor

The Marlin EEPROM editor provides an easy to use, feature-rich UI to edit your machine's configuration.

## Features

- Load & parse the EEPROM data out of the firmware
- Edit many of the values configured
- Save EEPROM changes on the printer with a minimal number of commands

- Storage of data on the OctoPrint server, so it can be viewed while printer is disconnected or printing.
- Backup feature:

  - Enabled saving configuration snapshots, restoring, downloading, uploading

- Display firmware info, including capability report

Be sure to [check out the screenshots](#screenshots) below for more details!

## Setup

Install via the bundled [plugin manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html) or manually using this URL:

    https://github.com/cp2004/OctoPrint-EEPROM-Marlin/releases/latest/download/release.zip

## Firmware requirements

This plugin requires three things:

- `EEPROM_CHITCHAT` function - make sure you have `#define EEPROM_CHITCHAT` in the config
- The `M503` command enabled - do not uncomment disabling it, leave it as `//#define DISABLE_M503`
- Of course, EEPROM to be enabled 🙂

## New in Marlin EEPROM Editor V3.0.0

A complete re-write of this plugin, now V3!

Featuring:

- Python processing & storage, eliminating performance issues in the UI.
- Storage of data on the OctoPrint server, so it can be viewed while the printer is disconnected or printing.
- Brand new UI, written from the ground up.
- All-new backup feature, allowing naming and storing of backups, so you can quickly swap between profiles and more.

## Screenhots

Firmware info overview
![Firmware Info](assets/firmware_info.png)

Configuration editor
![Configuration Editor](assets/config.png)

Backup feature
![Backup feature](assets/backup.png)

## Sponsors

* [@KenLucke](https://github.com/KenLucke)
* [@iFrostizz](https://github.com/iFrostizz)
* [@CmdrCody51](https://github.com/CmdrCody51)

As well as 5 others supporting me regularly through [GitHub Sponsors](https://github.com/sponsors/cp2004)!

## Supporting my efforts

I created this project in my spare time, so if you have found it useful or enjoyed using it then please consider [supporting it's development!](https://github.com/sponsors/cp2004). You can sponsor monthly or one time, for any amount you choose.
## ✏️ 🔧
