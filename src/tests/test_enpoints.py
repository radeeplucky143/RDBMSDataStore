import sys
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from os.path import dirname, abspath

sys.path.append(dirname(dirname(abspath(__file__))))

from main import app

client = TestClient(app)


@patch('core.DataStore.DataStore')
def test_get_object_success(mock_data_store):
    """Tests successful retrieval of an object from the DataStore."""

    key = "movie"
    tenant_id = "radeep"
    expected_data = {
        "tenant_id": tenant_id,
        "key": key,
        "value": "value",
        "size": 5,
        "ttl": 60,
        "creation_time": "2024-01-01T00:00:00",
        "expiry_time": "2025-01-01T00:00:00"
    }

    mock_data_store.return_value.tenantExists.return_value = True
    mock_data_store.return_value.getKey.return_value = [expected_data]
    mock_data_store.return_value.disconnect.return_value = None

    response = client.get(f"/api/object/{key}/{tenant_id}")
    print(response.json())

    assert response.status_code == 200
