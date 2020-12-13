# Marlin EEPROM Editor

This plugin is designed to get, change and save the values in the EEPROM of your Marlin Firmware based Machine.

## Setup

Install manually using this URL:

    https://github.com/cp2004/OctoPrint-EEPROM-Marlin/archive/master.zip

## Firmware requirements

This plugin requires that you have **both** these items in Marlin's `Configuration.h` file:

- `#define EEPROM_CHITCHAT`
- `//#define DISABLE_M503`

In other words, `EEPROM_CHITCHAT` and the M503 command must be enabled - comment out disabling it.

## COMING SOON

A complete re-write of this plugin is in the works. When it is ready for inital testing I'll be looking for willing beta-testers. If you're interested, let me know!

Featuring:

- Python processing & storage, eliminating performance issues in the UI.
- Storage of data on the OctoPrint server, so it can be viewed while the printer is disconnected or printing.
- Brand new UI, written from the ground up.
- All-new backup feature, allowing naming and storing of backups, so you can quickly swap between profiles and more.
- More optimisations and features may sneak in, stay tuned!
