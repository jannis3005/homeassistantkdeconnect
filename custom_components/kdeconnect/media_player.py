import logging
from homeassistant.components.media_player import MediaPlayerEntity
from homeassistant.components.media_player.const import (
    SUPPORT_PLAY,
    SUPPORT_PAUSE,
    SUPPORT_PLAY_MEDIA,
    SUPPORT_STOP,
    SUPPORT_VOLUME_SET,
    SUPPORT_PREVIOUS_TRACK,
    SUPPORT_NEXT_TRACK,
)
from homeassistant.const import STATE_PLAYING, STATE_PAUSED, STATE_IDLE

from jeepney import new_method_call

from . import DOMAIN, KDEConnect

_LOGGER = logging.getLogger(__name__)

SUPPORTED_FEATURES = (
        SUPPORT_PLAY
        | SUPPORT_PAUSE
        | SUPPORT_PLAY_MEDIA
        | SUPPORT_STOP
        | SUPPORT_VOLUME_SET
        | SUPPORT_PREVIOUS_TRACK
        | SUPPORT_NEXT_TRACK
)

async def async_setup_entry(hass, config_entry, async_add_entities):
    device_name = config_entry.data["device_name"]
    kdeconnect = KDEConnect(device_name)
    device = kdeconnect.get_device()
    async_add_entities([KDEConnectMediaPlayer(kdeconnect, device)], True)

class KDEConnectMediaPlayer(MediaPlayerEntity):
    def __init__(self, kdeconnect, device):
        self._kdeconnect = kdeconnect
        self._device = device
        self._state = STATE_IDLE

    def _invoke_device_action(self, action, params=None):
        if params is None:
            params = {}
        msg = new_method_call(self._device, 'invokeAction', action, params)
        self._kdeconnect.conn.send_message(msg)

    def _get_device_property(self, prop_name):
        msg = new_method_call(self._device, prop_name)
        return self._kdeconnect.conn.send_and_get_reply(msg)

    @property
    def name(self):
        return self._get_device_property('deviceName')

    @property
    def state(self):
        return self._state

    @property
    def supported_features(self):
        return SUPPORTED_FEATURES

    def play_media(self, media_type, media_id, **kwargs):
        self._invoke_device_action("playUrl", {"url": media_id})

    def media_play(self):
        self._invoke_device_action("play")

    def media_pause(self):
        self._invoke_device_action("pause")

    def media_stop(self):
        self._invoke_device_action("stop")

    def media_previous_track(self):
        self._invoke_device_action("previous")

    def media_next_track(self):
        self._invoke_device_action("next")

    def set_volume_level(self, volume):
        self._invoke_device_action("setVolume", {"volume": int(volume * 100)})
