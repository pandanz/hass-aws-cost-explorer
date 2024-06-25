# AWS Cost Explorer

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

![Project Maintenance][maintenance-shield]

_Integration to integrate with [hass-aws-cost-explorer][hass-aws-cost-explorer]._

**This integration will set up the following platforms.**

Platform | Description
-- | --
`binary_sensor` | Show something `True` or `False`.
`sensor` | Show info from blueprint API.
`switch` | Switch something `True` or `False`.

## Installation
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

1. Open HACS Settings and add this repository (https://github.com/pandanz/hass-aws-cost-explorer/)
   as a Custom Repository (use **Integration** as the category).
2. The `hass-aws-cost-explorer` page should automatically load (or find it in the HACS Store)
3. Click `Install`

Alternatively, click on the button below to add the repository:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?category=Integration&repository=hass-aws-cost-explorer&owner=pandanz)

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[hass-aws-cost-explorer]: https://github.com/pandanz/hass-aws-cost-explorer
[commits-shield]: https://img.shields.io/github/commit-activity/y/pandanz/hass-aws-cost-explorer.svg?style=for-the-badge
[commits]: https://github.com/pandanz/hass-aws-cost-explorer/commits/main
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/pandanz/hass-aws-cost-explorer.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-pandanz-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/pandanz/hass-aws-cost-explorer.svg?style=for-the-badge
[releases]: https://github.com/pandanz/hass-aws-cost-explorer/releases
