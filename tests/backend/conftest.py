import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

server_path = Path(__file__).parent.parent.parent / "server"
sys.path.insert(0, str(server_path))

from main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def sample_ticket():
    """Sample ticket structure for reference."""
    return {
        "id": "TKT-001",
        "subject": "VPN disconnects every 10 minutes on corporate WiFi",
        "status": "Resolved",
        "priority": "High",
        "category": "Network",
        "assigned_to": "AGT-004",
        "created_at": "2025-11-05T08:30:00",
    }


@pytest.fixture
def sample_agent():
    """Sample agent structure for reference."""
    return {
        "id": "AGT-001",
        "name": "Marcus Rivera",
        "role": "L1",
        "status": "Available",
    }
