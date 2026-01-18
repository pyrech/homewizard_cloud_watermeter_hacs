"""Support for HomeWizard Cloud Watermeter sensors."""
from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from .const import DOMAIN, CONF_EMAIL

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor platform."""
    email = entry.data.get(CONF_EMAIL)
    async_add_entities([HomeWizardWaterSensor(email)], True)

class HomeWizardWaterSensor(SensorEntity):
    """Representation of a HomeWizard Watermeter sensor."""

    _attr_name = "HomeWizard Water Consumption"
    _attr_native_unit_of_measurement = "L"
    _attr_device_class = SensorDeviceClass.WATER
    _attr_state_class = SensorStateClass.TOTAL_INCREASING

    def __init__(self, email):
        """Initialize the sensor."""
        self._email = email
        self._attr_unique_id = f"hw_watermeter_{email}"

    async def async_update(self):
        """Fetch new state data for the sensor."""
        # This is where the GraphQL logic will go
        # Temporary mock value for testing
        self._attr_native_value = 5678