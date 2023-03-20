"""The KDE Connect integration."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.typing import ConfigType, HomeAssistantType
from homeassistant.helpers import discovery

from .const import (
    DOMAIN,
    CONF_NAME,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["media_player", "device_tracker"]

async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Set up the KDE Connect entry."""
    kdeconnect = hass.data[DOMAIN]["kdeconnect"]
    devices = hass.data[DOMAIN]["devices"]
    name = entry.data[CONF_NAME]

    async def async_discover_device_callback(device):
        """Handle the discovery of a new KDE Connect device."""
        device_name = device["name"]
        device_id = device["id"]
        _LOGGER.debug("Discovered KDE Connect device '%s' (%s)", device_name, device_id)

        if device_id not in devices:
            # Add the device
            devices.append(device_id)

            # Load the media player platform
            hass.async_create_task(
                discovery.async_load_platform(
                    hass,
                    "media_player",
                    DOMAIN,
                    {"name": name, "device_id": device_id},
                    entry.data,
                )
            )

            # Load the device tracker platform
            hass.async_create_task(
                discovery.async_load_platform(
                    hass,
                    "device_tracker",
                    DOMAIN,
                    {"name": name, "device_id": device_id},
                    entry.data,
                )
            )

    # Subscribe to device discovery events
    async_dispatcher_connect(
        hass, f"{DOMAIN}_discovered_device", async_discover_device_callback
    )

    # Discover devices
    for device in await hass.async_add_executor_job(kdeconnect.discover):
        async_discover_device_callback(device)

    return True

async def async_setup(hass: HomeAssistantType, config: ConfigType):
    """Set up the KDE Connect integration."""
    hass.data[DOMAIN] = {"devices": []}

    return True

