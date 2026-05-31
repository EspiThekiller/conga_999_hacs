# Cecotec Conga 999 Map integration for Home Assistant

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=EspiThekiller&repository=conga_999_hacs&category=integration)

This integration aims to manage the **Cecotec Conga 999 Map** vacuum cleaner in Home Assistant using local Tuya protocol.

The author of this project categorically rejects any and all responsibility related to vacuums managed by this integration.

## HACS Installation

1. Navigate to `HACS > Integrations`
2. Click the 3 dots in the top right corner and select `Custom repositories`
3. Add the URL of this repository: `https://github.com/EspiThekiller/conga_999_hacs` with category `Integration`
4. Search for `Conga 999 Map` in HACS and click `Download`
5. Restart Home Assistant

## Configuration

1. Navigate to `Settings > Devices & Services` and then click `Add Integration`
2. Search for `Conga 999 Map`
3. Enter your vacuum's IP Address, Device ID, and Local Key.
   *(Note: Because this relies on Tuya local control, you must obtain your Device ID and Local Key by linking your device via a Tuya Developer account. You can follow standard Tuya Local extraction tutorials for this).*

## Supported devices

This integration has been tested with the following vacuum cleaners:

| Model name | Supported? |
| ---------- | ---------- |
| Conga 999 Map | ✅ Yes! |
