import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, CONF_ACCESS_KEY, CONF_SECRET_KEY, CONF_TAG, CONF_SCAN_INTERVAL

class AWSBillingConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="AWS Cost Explorer", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_ACCESS_KEY): str,
                vol.Required(CONF_SECRET_KEY): str,
                vol.Optional(CONF_TAG): str,
                vol.Optional(CONF_SCAN_INTERVAL, default=240): int
            })
        )
    
#     @staticmethod
#     @callback
#     def async_get_options_flow(config_entry):
#         return AWSBillingOptionsFlowHandler(config_entry)

# class AWSBillingOptionsFlowHandler(config_entries.OptionsFlow):
#     def __init__(self, config_entry):
#         self.config_entry = config_entry

#     async def async_step_init(self, user_input=None):
#         if user_input is not None:
#             return self.async_create_entry(title="", data=user_input)

#         return self.async_show_form(
#             step_id="init",
#             data_schema=vol.Schema({
#                 vol.Optional(CONF_ACCESS_KEY, default=self.config_entry.options.get(CONF_ACCESS_KEY, "Enter Access Key")): str,
#                 vol.Optional(CONF_SECRET_KEY, default=self.config_entry.options.get(CONF_SECRET_KEY, "Enter Secret Key")): str,
#                 vol.Optional(CONF_TAG, default=self.config_entry.options.get(CONF_TAG, "Enter Tag")): str,
#                 vol.Optional(CONF_POLL, default=self.config_entry.options.get(CONF_POLL, False)): bool
#             })
#         )
