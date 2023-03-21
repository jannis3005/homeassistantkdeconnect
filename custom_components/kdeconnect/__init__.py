import logging
import voluptuous as vol
from homeassistant import config_entries, core

from jeepney import DBusAddress, new_method_call
from jeepney.integrate.blocking import connect_and_authenticate

_LOGGER = logging.getLogger(__name__)
DOMAIN = "kdeconnect"


class KDEConnect:
    def __init__(self, device_name):
        self.device_name = device_name
        self.conn = connect_and_authenticate(bus='SESSION')
        self.kdeconnectd_addr = DBusAddress('/modules/kdeconnect',
                                            'org.kde.kdeconnect.daemon',
                                            'org.kde.kdeconnect')

    def get_device(self):
        devices_msg = new_method_call(self.kdeconnectd_addr, 'devices')
        devices = self.conn.send_and_get_reply(devices_msg)

        for device_id in devices:
            device_addr = DBusAddress(f'/modules/kdeconnect/devices/{device_id}',
                                      'org.kde.kdeconnect.device',
                                      'org.kde.kdeconnect')
            device_name_msg = new_method_call(device_addr, 'deviceName')
            device_name = self.conn.send_and_get_reply(device_name_msg)

            if device_name == self.device_name:
                return device_addr

        return None

    def pair_device(self):
        device = self.get_device()
        if device:
            pair_request_msg = new_method_call(device, 'requestPair')
            self.conn.send_message(pair_request_msg)
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
