import logging
from azure.monitor.opentelemetry import configure_azure_monitor


configure_azure_monitor(logger_name="journal")
logger = logging.getLogger("journal")