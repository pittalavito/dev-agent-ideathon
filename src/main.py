import logging

from client.client import intialize_clients
from agent.devagent import init_dev_agent

from ui.app import homePage

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format="[%(levelname)s]: %(message)s")

# Initialize at startup
intialize_clients()
init_dev_agent()

# Start the UI
homePage()
