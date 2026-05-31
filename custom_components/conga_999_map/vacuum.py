from homeassistant.components.vacuum import (
    StateVacuumEntity,
    VacuumEntityFeature,
    STATE_CLEANING,
    STATE_DOCKED,
    STATE_IDLE,
    STATE_PAUSED,
    STATE_ERROR,
    STATE_RETURNING,
)
import tinytuya
import logging

from .const import DOMAIN, CONF_DEVICE_ID, CONF_IP_ADDRESS, CONF_LOCAL_KEY

_LOGGER = logging.getLogger(__name__)

SUPPORTED_FEATURES = (
    VacuumEntityFeature.START
    | VacuumEntityFeature.PAUSE
    | VacuumEntityFeature.STOP
    | VacuumEntityFeature.RETURN_HOME
    | VacuumEntityFeature.BATTERY
    | VacuumEntityFeature.LOCATE
    | VacuumEntityFeature.STATUS
)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Conga vacuum from a config entry."""
    device_id = config_entry.data[CONF_DEVICE_ID]
    ip_address = config_entry.data[CONF_IP_ADDRESS]
    local_key = config_entry.data[CONF_LOCAL_KEY]
    
    device = await hass.async_add_executor_job(
        lambda: tinytuya.VacuumDevice(device_id, ip_address, local_key)
    )
    device.set_version(3.3)
    
    async_add_entities([CongaVacuum(device, config_entry.title)])

class CongaVacuum(StateVacuumEntity):
    """Representation of a Conga 999 vacuum cleaner."""

    def __init__(self, device, name):
        """Initialize the vacuum."""
        self._device = device
        self._name = name
        self._state = STATE_IDLE
        self._battery_level = None
        self._available = False
        
        # Default Tuya DPs for vacuums (these might need fine-tuning for Conga 999 specifically)
        self.dp_switch = "1"
        self.dp_pause = "2"
        self.dp_status = "3"
        self.dp_battery = "4"
        self.dp_locate = "5"

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def state(self):
        """Return the state of the vacuum."""
        return self._state

    @property
    def battery_level(self):
        """Return the battery level of the vacuum."""
        return self._battery_level

    @property
    def available(self):
        """Return True if entity is available."""
        return self._available

    @property
    def supported_features(self):
        """Flag vacuum cleaner features that are supported."""
        return SUPPORTED_FEATURES

    def update(self):
        """Update the status of the vacuum."""
        try:
            data = self._device.status()
            if data and "dps" in data:
                dps = data["dps"]
                self._available = True
                
                # Update battery
                if self.dp_battery in dps:
                    self._battery_level = int(dps[self.dp_battery])
                
                # Update status
                if self.dp_status in dps:
                    status = dps[self.dp_status]
                    if status in ["smart", "cleaning", "wall_follow", "spiral"]:
                        self._state = STATE_CLEANING
                    elif status in ["chargego", "charging"]:
                        self._state = STATE_RETURNING if status == "chargego" else STATE_DOCKED
                    elif status in ["standby", "idle"]:
                        self._state = STATE_IDLE
            else:
                self._available = False
        except Exception as e:
            _LOGGER.error("Error updating Conga vacuum: %s", e)
            self._available = False

    def start(self):
        """Start or resume the cleaning task."""
        self._device.set_value(self.dp_switch, True)

    def pause(self):
        """Pause the cleaning task."""
        self._device.set_value(self.dp_switch, False)

    def stop(self, **kwargs):
        """Stop the cleaning task."""
        self._device.set_value(self.dp_switch, False)

    def return_to_base(self, **kwargs):
        """Set the vacuum cleaner to return to the dock."""
        self._device.set_value(self.dp_switch, False)
        self._device.set_value(self.dp_status, "chargego")

    def locate(self, **kwargs):
        """Locate the vacuum cleaner."""
        self._device.set_value(self.dp_locate, True)
