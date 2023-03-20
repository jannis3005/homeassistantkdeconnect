"""Support for KDE Connect media players."""
import logging

from homeassistant.components.media_player import MediaPlayerEntity
from homeassistant.components.media_player.const import (
    SUPPORT_PAUSE,
    SUPPORT_PLAY,
    SUPPORT_PREVIOUS_TRACK,
    SUPPORT_NEXT_TRACK,
    SUPPORT_STOP,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SUPPORT_KDE_CONNECT = (
    SUPPORT_PAUSE
    | SUPPORT_PLAY
    | SUPPORT_PREVIOUS_TRACK
    | SUPPORT_NEXT_TRACK
    | SUPPORT_STOP
)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the KDE Connect media player platform."""

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the KDE Connect media player from a config entry."""

    kdeconnect = hass.data[DOMAIN]["kdeconnect"]
    device_id = entry.data["device_id"]
    name = entry.data["name"]
    coordinator = hass.data[DOMAIN]["coordinators"][device_id]

    async_add_entities([KDEConnectMediaPlayer(coordinator, name)], True)

class KDEConnectMediaPlayer(CoordinatorEntity, MediaPlayerEntity):
    """Representation of a KDE Connect media player."""

    def __init__(self, coordinator, name):
        """Initialize the KDE Connect media player."""
        super().__init__(coordinator)
        self._name = name
        self._state = None
        self._media_title = None
        self._media_artist = None
        self._media_album_name = None

    @property
    def name(self):
        """Return the name of the media player."""
        return self._name

    @property
    def supported_features(self):
        """Return the features supported by the media player."""
        return SUPPORT_KDE_CONNECT

    @property
    def state(self):
        """Return the state of the media player."""
        return self._state

    @property
    def media_title(self):
        """Return the current media title."""
        return self._media_title

    @property
    def media_artist(self):
        """Return the current media artist."""
        return self._media_artist

    @property
    def media_album_name(self):
        """Return the current media album name."""
        return self._media_album_name

    async def async_media_play(self):
        """Send the play command."""
        await self.coordinator.play()

    async def async_media_pause(self):
        """Send the pause command."""
        await self.coordinator.pause()

    async def async_media_stop(self):
        """Send the stop command."""
        await self.coordinator.stop()

    async def async_media_previous_track(self):
        """Send the previous track command."""
        await self.coordinator.previous_track()

    async def async_media_next_track(self):
        """Send the next track command."""
        await self.coordinator.next_track()

    async def async_update(self):
        """Update the state of the media player."""
        await self.coordinator.async_request_refresh()

        self._state = None
        self._media_title = None
        self._media_artist = None
        self._media_album_name = None

        state = self.coordinator.data.get("state")
        if state is not None:
            self._state = state.lower()

        media_title = self.coordinator.data.get("media_title")
        if media_title is not None:
            self._media_title = media_title

        media_artist = self.coordinator.data.get("media_artist")
        if media_artist is not None:
           
        self._media_artist = media_artist

    media_album_name = self.coordinator.data.get("media_album_name")
    if media_album_name is not None:
        self._media_album_name = media_album_name
