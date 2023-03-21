import logging
from homeassistant.helpers.entity import Entity
from homeassistant.const import DEVICE_CLASS_BATTERY

from jeepney import new_method_call

from . import DOMAIN, KDEConnect

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    device_name = config_entry.data["device_name"]
    kdeconnect = KDEConnect(device_name)
    device = kdeconnect.get_device()
    async_add_entities([KDEConnectBatterySensor(kdeconnect, device), KDEConnectNetworkSensor(device)], True)

class KDEConnectBatterySensor(Entity):
    def __init__(self, kdeconnect, device):
        self._kdeconnect = kdeconnect
        self._device = device
        self._state = None

    def _get_device_property(self, prop_name):
        msg = new_method_call(self._device, prop_name)
        return self._kdeconnect.conn.send_and_get_reply(msg)

    @property
    def name(self):
        return f"{self._get_device_property('deviceName')} Battery"

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
        battery_charge_msg = new_method_call(self._device, 'charge')
        self._state = self._kdeconnect.conn.send_and_get_reply(battery_charge_msg)

class KDEConnectNetworkSensor(Entity):
    def __init__(self, device):
        self._device = device
        self._state = None

    @property
    def name(self):
        return f"{self._device.deviceName()} Network"

    @property
    def state(self):
        return self._state
