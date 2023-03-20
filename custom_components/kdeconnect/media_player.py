import logging
import dbus
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
    async_add_entities([KDEConnectMediaPlayer(device)], True)

class KDEConnectMediaPlayer(MediaPlayerEntity):
    def __init__(self, device):
        self._device = device
        self._state = STATE_IDLE

    @property
    def name(self):
        return self._device.deviceName()

    @property
    def state(self):
        return self._state

    @property
    def supported_features(self):
        return SUPPORTED_FEATURES

    def play_media(self, media_type, media_id, **kwargs):
        self._device.invokeAction("playUrl", {"url": media_id})

    def media_play(self):
        self._device.invokeAction("play")

    def media_pause(self):
        self._device.invokeAction("pause")

    def media_stop(self):
        self._device.invokeAction("stop")

    def media_previous_track(self):
        self._device.invokeAction("previous")

    def media_next_track(self):
        self._device.invokeAction("next")

    def set_volume_level(self, volume):
        self._device.invokeAction("setVolume", {"volume": int(volume * 100)})
