import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
from .const import DOMAIN

# Set up the logger
_LOGGER = logging.getLogger(__name__)


from homeassistant.helpers import (
    config_validation as cv
)

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    return True

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    # Forward the setup to the sensor platform
    _LOGGER.debug("Starting async_setup_entry for AWS Billing")
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, "sensor")
    )
    return True

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    await hass.config_entries.async_forward_entry_unload(config_entry, "sensor")
    return True