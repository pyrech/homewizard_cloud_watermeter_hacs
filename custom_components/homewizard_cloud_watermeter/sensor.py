import logging
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]

    if not coordinator.data:
        _LOGGER.error("No devices found, sensors will not be created")

    entities = []

    # Create a sensor for each homewizard device
    for value in coordinator.data:
        entities.append(HomeWizardCloudWaterSensor(coordinator, value))

    async_add_entities(entities)

class HomeWizardCloudWaterSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, data):
        super().__init__(coordinator)

        self._daily_total = data["daily_total"]
        self._device = data["device"]
        self._attr_name = "Daily usage"
        self._attr_unique_id = f"{self._device['sanitized_identifier']}_daily_total"
        self._attr_device_class = SensorDeviceClass.WATER
        self._attr_native_unit_of_measurement = data["unit"]

        # Use TOTAL for daily values that reset at midnight
        self._attr_state_class = SensorStateClass.TOTAL

    @property
    def device_info(self):
        """Return device information about this entity."""
        return {
            "identifiers": {(DOMAIN, self._device["sanitized_identifier"])},
            "name": self._device.get("name"),
            "manufacturer": "HomeWizard",
            "model": self._device.get("model"),
        }

    @property
    def native_value(self):
        """Return the state of the sensor as a float."""
        if not self._daily_total:
            return None

        try:
            return float(self._daily_total)
        except ValueError:
            _LOGGER.warning("Could not convert value '%s' to float", self._daily_total)
            return None
