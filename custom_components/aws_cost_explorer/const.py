"""Constants for aws_billing_integration."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

NAME = "AWS Cost Explorer"
DOMAIN = "aws_cost_explorer"
VERSION = "0.1"

CONF_ACCESS_KEY = "access_key"
CONF_SECRET_KEY = "secret_key"
CONF_TAG = "tag"
CONF_SCAN_INTERVAL = "scan_interval_minutes"

ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"
