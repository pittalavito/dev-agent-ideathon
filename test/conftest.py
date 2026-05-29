import sys
from pathlib import Path

import pytest

# Ensure src/ is on the path when running pytest from the project root
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from client.client import init_clients


@pytest.fixture(scope="session", autouse=True)
def clients():
    """Initialize LLM clients once per test session."""
    init_clients()
