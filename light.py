"""Platform for light integration."""
import logging
import voluptuous as vol
from pywizlight import wizlight

import homeassistant.helpers.config_validation as cv
# Import the device class from the component that you want to support
from homeassistant.components.light import (
    ATTR_BRIGHTNESS, PLATFORM_SCHEMA, Light)
from homeassistant.const import CONF_IP_ADDRESS

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_IP_ADDRESS): cv.string,
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Awesome Light platform."""
    # Assign configuration variables.
    # The configuration check takes care they are present.
    ip = config[CONF_IP_ADDRESS]

    bulb = wizlight(ip)

    # Add devices
    add_entities(AwesomeLight(bulb))


class AwesomeLight(Light):
    """Representation of WiZ Light bulb"""

    def __init__(self, bulb):
        """Initialize an WiZLight."""
        self._light = bulb
        self._state = None
        self._brightness = None

    @property
    def brightness(self):
        """Return the brightness of the light. """
        return self._brightness

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._state

    def turn_on(self, **kwargs):
        """Instruct the light to turn on."""
        self._light.brightness = self.hex_to_percent(kwargs.get(ATTR_BRIGHTNESS, 255))
        self._light.turn_on()

    def turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        self._light.turn_off()

    def update(self):
        """Fetch new state data for this light.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._light.status
        self._brightness = self._light.getBrightness

    def hex_to_percent(self, hex):
        return (hex/255)*100

    def percent_to_hex(self, percent):
        return (percent / 100)*255