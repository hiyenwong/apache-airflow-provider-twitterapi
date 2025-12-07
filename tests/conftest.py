"""Setup configuration for tests."""

import pytest


@pytest.fixture
def mock_airflow_connection():
    """Mock Airflow connection for testing."""
    class MockConnection:
        def __init__(self):
            self.password = "test_api_key"
            self.extra_dejson = {}
    
    return MockConnection()
