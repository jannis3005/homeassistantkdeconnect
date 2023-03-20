import logging
import dbus
from homeassistant import config_entries, core

_LOGGER = logging.getLogger(__name__)
DOMAIN = "kdeconnect"

class KDEConnect:
    def __init__(self, device_name):
        self.device_name = device_name
        self.bus = dbus.SessionBus()
        self.kdeconnectd_proxy = self.bus.get_object("org.kde.kdeconnect", "/modules/kdeconnect")
        self.kdeconnectd_iface = dbus.Interface(self.kdeconnectd_proxy, "org.kde.kdeconnect.daemon")

    def get_device(self):
        devices = self.kdeconnectd_iface.devices()
        for device_id in devices:
            device_proxy = self.bus.get_object("org.kde.kdeconnect", f"/modules/kdeconnect/devices/{device_id}")
            device_iface = dbus.Interface(device_proxy, "org.kde.kdeconnect.device")
            if device_iface.deviceName() == self.device_name:
                return device_iface
        return None

    def pair_device(self):
        device = self.get_device()
        if device:
            device.requestPair()
        else:
            _LOGGER.error(f"Device with name '{self.device_name}' not found")

async def async_setup(hass: core.HomeAssistant, config: dict):
    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_IMPORT}
        )
    )
    return True

class KDEConnectConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            kdeconnect = KDEConnect(user_input["device_name"])
            kdeconnect.pair_device()
            return self.async_create_entry(title="KDE Connect", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("device_name", default=""): str,
                }
            ),
        )
