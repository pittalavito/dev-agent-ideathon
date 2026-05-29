import logging

from client.client import init_clients
from agent.devagent import init_dev_agent

from ui.app import StartHomePage

# Set up logging configuration (force=True prevents duplicate handlers on Streamlit reruns)
logging.basicConfig(level=logging.INFO, format="[%(levelname)s]: %(message)s", force=True)

# Initialize at startup
init_clients()
init_dev_agent()

# Start the UI
StartHomePage()
