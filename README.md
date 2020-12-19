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

Be sure to [check out the screenshots](#Screenshots) below for more details!

---

# Installing the release candidate:
:tada: There is a new major version of this plugin available, currently in RC phase.

It would be great if you could test it, directions for install can be found below.

:warning: This is a pre-release version of Marlin EEPROM Editor :warning: 
You should only run this if you are OK with things not working perfectly. I have extensively tested this, but this is what RC phases are for, to pick up on bugs before the wider roll out. **It should not break anything to install it**, it just won't work itself.

Install using the following URL in OctoPrint's plugin manager > get more > ...from URL:
```
https://github.com/cp2004/OctoPrint-EEPROM-Marlin/archive/3.0.0rc3.zip
```
Once that is installed (and in OP 1.5.0+) you will be able to select 'release candidate' as the release channel (under 'Software Update'), to get future RC updates automatically:
![image](https://user-images.githubusercontent.com/31997505/102026390-722e7200-3d95-11eb-80e1-05197b9868f0.png)

For a full overview of the features that have gone into this release, please read the [release notes](https://github.com/cp2004/OctoPrint-EEPROM-Marlin/releases/tag/3.0.0rc1)

---

## Setup

Install manually using this URL:

    https://github.com/cp2004/OctoPrint-EEPROM-Marlin/archive/master.zip

## Firmware requirements

This plugin requires that you have **both** these items in Marlin's `Configuration.h` file:

- `#define EEPROM_CHITCHAT`
- `//#define DISABLE_M503`

In other words, `EEPROM_CHITCHAT` and the M503 command must be enabled - comment out disabling it.

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
