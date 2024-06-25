import logging
import boto3
from datetime import datetime, timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorStateClass
from homeassistant.helpers.restore_state import RestoreEntity
from .const import DOMAIN, CONF_ACCESS_KEY, CONF_SECRET_KEY, CONF_TAG, CONF_SCAN_INTERVAL

# Set up the logger
_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=240)

def create_boto3_client(service_name, access_key, secret_key):
    return boto3.client(service_name, aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name="us-east-1")

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    _LOGGER.debug("Setting up AWSBillingSensor...")
    ce = await hass.async_add_executor_job(
        create_boto3_client,
        'ce', 
        config_entry.data[CONF_ACCESS_KEY],
        config_entry.data[CONF_SECRET_KEY],
    )

    hass.data[DOMAIN] = {"client": ce}
    
    async_add_entities([AWSBillingCurrentSensor(config_entry.data, ce)])
    async_add_entities([AWSBillingForecastSensor(config_entry.data, ce)])
    if CONF_TAG in config_entry.data:
        async_add_entities([AWSBillingByTagSensor(config_entry.data, ce)])

class AWSBillingCurrentSensor(SensorEntity, RestoreEntity):
    def __init__(self, config, ce):
        self._config = config
        self._attr_name = "AWS Billing Current Month"
        self._state = None
        self._ce = ce
        self._currency = "USD"
        self._attr_extra_state_attributes = {}
        self._attr_state_class = SensorStateClass.TOTAL

    async def async_added_to_hass(self):
        """Run when entity about to be added to hass."""
        await super().async_added_to_hass()
        state = await self.async_get_last_state()
        if state:
            self._state = state.state

    @property
    def should_poll(self):
        return True

    @property
    def name(self):
        return self._attr_name

    @property
    def state(self):
        return self._state
    
    @property
    def icon(self):
        return "mdi:aws"

    @property
    def extra_state_attributes(self):
        return self._attr_extra_state_attributes

    @property
    def unique_id(self):
        return f"sensor.{self._attr_name}"

    async def async_update(self):
        # Define a function to fetch AWS billing information
        def fetch_current_aws_billing():
            now = datetime.now()
            start_date = now.replace(day=1).strftime('%Y-%m-%d')
            if now.month == 12:
                end_date = now.replace(year=now.year+1, month=1, day=1) - timedelta(days=1)
            else:
                end_date = now.replace(month=now.month+1, day=1) - timedelta(days=1)
            end_date = end_date.strftime('%Y-%m-%d')

            response_current = self._ce.get_cost_and_usage(
                    TimePeriod={
                        'Start': start_date,
                        'End': end_date
                    },
                    Granularity='MONTHLY',
                    Metrics=['UnblendedCost'],
                )

            current_cost = response_current['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']
            current_cost = round(float(current_cost), 2)

            return current_cost
        
        current_cost = await self.hass.async_add_executor_job(fetch_current_aws_billing)
        _LOGGER.debug(f"Current Month Bill {current_cost}")

        # Update sensor state and attributes
        self._state = current_cost
        self._attr_extra_state_attributes['currency'] = self._currency

class AWSBillingByTagSensor(SensorEntity, RestoreEntity):
    def __init__(self, config, ce):
        self._config = config
        self._attr_name = "AWS Billing Current By Tag"
        self._state = None
        self._ce = ce
        self._currency = "USD"
        self._attr_extra_state_attributes = {}
        self._attr_state_class = SensorStateClass.TOTAL

    async def async_added_to_hass(self):
        """Run when entity about to be added to hass."""
        await super().async_added_to_hass()
        state = await self.async_get_last_state()
        if state:
            self._state = state.state

    @property
    def should_poll(self):
        return True

    @property
    def name(self):
        return self._attr_name

    @property
    def state(self):
        return self._state
    
    @property
    def icon(self):
        return "mdi:aws"

    @property
    def extra_state_attributes(self):
        return self._attr_extra_state_attributes

    @property
    def unique_id(self):
        return f"sensor.{self._attr_name}"

    async def async_update(self):
        # Define a function to fetch AWS billing information
        def fetch_current_by_tag_aws_billing():
            now = datetime.now()
            start_date = now.replace(day=1).strftime('%Y-%m-%d')
            if now.month == 12:
                end_date = now.replace(year=now.year+1, month=1, day=1) - timedelta(days=1)
            else:
                end_date = now.replace(month=now.month+1, day=1) - timedelta(days=1)
            end_date = end_date.strftime('%Y-%m-%d')

            tag_name = self._config[CONF_TAG]

            response_by_tag = self._ce.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date,
                    'End': end_date
                },
                Granularity='MONTHLY',
                Metrics=['UnblendedCost'],
                GroupBy=[
                    {
                        'Type': 'TAG',
                        'Key': tag_name
                    },
                ]
            )

            costs_by_tag = {}
            for result in response_by_tag['ResultsByTime'][0]['Groups']:
                key = result['Keys'][0]
                if key == f"{tag_name}$":
                    tag_value = "untagged"
                else:
                    tag_value = key.replace(f'{tag_name}$', '')

                cost = result['Metrics']['UnblendedCost']['Amount']
                costs_by_tag[tag_value] = round(float(cost), 2)

            return costs_by_tag

        # Execute the blocking function asynchronously
        costs_by_tag = await self.hass.async_add_executor_job(fetch_current_by_tag_aws_billing)

        # Update sensor state and attributes
        self._attr_extra_state_attributes['currency'] = self._currency
        for tag, cost in costs_by_tag.items():
            if tag == "untagged":
                self._state = cost
            else:
                self._attr_extra_state_attributes[tag] = cost

class AWSBillingForecastSensor(SensorEntity, RestoreEntity):
    def __init__(self, config, ce):
        self._config = config
        self._attr_name = "AWS Billing Forecast Month"
        self._state = None
        self._currency = "USD"
        self._ce = ce
        self._attr_extra_state_attributes = {}
        self._attr_state_class = SensorStateClass.TOTAL

    async def async_added_to_hass(self):
        """Run when entity about to be added to hass."""
        await super().async_added_to_hass()
        state = await self.async_get_last_state()
        if state:
            self._state = state.state

    @property
    def should_poll(self):
        return True

    @property
    def name(self):
        return self._attr_name

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return "mdi:aws"

    @property
    def extra_state_attributes(self):
        return self._attr_extra_state_attributes

    @property
    def unique_id(self):
        return f"sensor.{self._attr_name}"

    async def async_update(self):
        # Define a function to fetch AWS billing information
        def fetch_forecasted_aws_billing():
            now = datetime.now()
            start_date = now.strftime('%Y-%m-%d')
            if now.month == 12:
                end_date = now.replace(year=now.year+1, month=1, day=1) - timedelta(days=1)
            else:
                end_date = now.replace(month=now.month+1, day=1) - timedelta(days=1)
            end_date = end_date.strftime('%Y-%m-%d')

            response = self._ce.get_cost_forecast(
                TimePeriod={
                    'Start': start_date,
                    'End': end_date
                },
                Metric='UNBLENDED_COST',
                Granularity='MONTHLY',
            )

            forecasted_cost = response['Total']['Amount']
            forecasted_cost = round(float(forecasted_cost), 2)
            return forecasted_cost

        # Execute the blocking function asynchronously
        cost = await self.hass.async_add_executor_job(fetch_forecasted_aws_billing)
        _LOGGER.debug(f"Forecasted Month Bill {cost}")

        # Update sensor state and attributes
        self._state = cost
        self._attr_extra_state_attributes['currency'] = self._currency