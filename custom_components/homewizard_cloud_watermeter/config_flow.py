"""Config flow for HomeWizard Cloud Watermeter integration."""
import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_EMAIL, CONF_PASSWORD
import homeassistant.helpers.config_validation as cv

class HomeWizardCloudConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HomeWizard Cloud Watermeter."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            # TODO: Add API validation logic here
            return self.async_create_entry(
                title=user_input[CONF_EMAIL], 
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_EMAIL): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
            }),
            errors=errors,
        )