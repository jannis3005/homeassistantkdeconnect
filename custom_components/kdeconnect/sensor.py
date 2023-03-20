import logging
import dbus
from homeassistant.helpers.entity import Entity
from homeassistant.const import DEVICE_CLASS_BATTERY

from . import DOMAIN, KDEConnect

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    device_name = config_entry.data["device_name"]
    kdeconnect = KDEConnect(device_name)
    device = kdeconnect.get_device()
    async_add_entities([KDEConnectBatterySensor(device), KDEConnectNetworkSensor(device)], True)

class KDEConnectBatterySensor(Entity):
    def __init__(self, device):
        self._device = device
        self._state = None

    @property
    def name(self):
        return f"{self._device.deviceName()} Battery"

    @property
    def device_class(self):
        return DEVICE_CLASS_BATTERY

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return "%"

    def update(self):
        battery_iface = dbus.Interface(self._device, "org.kde.kdeconnect.device.battery")
        self._state = battery_iface.charge()

class KDEConnectNetworkSensor(Entity):
    def __init__(self, device):
        self._device = device
        self._state = None

    @property
    def name(self):
        return f"{self._device.deviceName()} Network"

    @property
    def state(self):
        return self
