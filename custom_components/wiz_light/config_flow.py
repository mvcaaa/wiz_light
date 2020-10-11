"""Config flow for WiZ Light integration."""
from pywizlight import discovery

from homeassistant import config_entries
from homeassistant.helpers import config_entry_flow

from .const import DOMAIN


async def _async_has_devices(hass) -> bool:
    """Return if there are devices that can be discovered."""
    bulbs = await discovery.find_wizlights(discovery)
    devices = await hass.async_add_executor_job(bulbs)
    return len(devices) > 0


config_entry_flow.register_discovery_flow(
    DOMAIN,
    "WiZ Light integration",
    _async_has_devices,
    config_entries.CONN_CLASS_UNKNOWN,
)
