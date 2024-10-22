import sys
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from os.path import dirname, abspath
from datetime import datetime

sys.path.append(dirname(dirname(abspath(__file__))))

from main import app

client = TestClient(app)


@patch('api.endpoints.DataStore')
def test_get_object_success(mock_data_store):
    """Tests successful retrieval of an object from the DataStore."""

    key = "movie"
    tenant_id = "radeep"
    getkey_data = [(1, tenant_id, key, "value", 5, 60, datetime.fromisoformat("2024-01-01T00:00:00"), datetime.fromisoformat("2025-01-01T00:00:00"))]
    expected_data = {'tenant_id': 'radeep', 'key': 'movie', 'value': 'value', 'size': 5, 'ttl': 60, 'creation_time': '2024-01-01T00:00:00', 'expiry_time': '2025-01-01T00:00:00'}

    mock_data_store.return_value.tenantExists.return_value = True
    mock_data_store.return_value.getKey.return_value = getkey_data
    mock_data_store.return_value.disconnect.return_value = None

    response = client.get(f"/api/object/{key}/{tenant_id}")

    assert response.status_code == 200
    assert response.json() == expected_data


@patch('api.endpoints.DataStore')
def test_get_object_user_not_found(mock_data_store):
    """User Not found case check"""

    key = "movie"
    tenant_id = "radeep"
    expected_data = {'message': f'Dear {tenant_id}, you were not registered/exists in the database.'}


    mock_data_store.return_value.tenantExists.return_value = False
    mock_data_store.return_value.disconnect.return_value = None

    response = client.get(f"/api/object/{key}/{tenant_id}")

    assert response.status_code == 404
    assert response.json() == expected_data


@patch('api.endpoints.DataStore')
def test_get_object_exception(mock_data_store):
    """User Not found case check"""

    key = "movie"
    tenant_id = "radeep"
    expected_data = {"error": "error occured while creating."}

    mock = mock_data_store.return_value
    mock.tenantExists.side_effect = Exception("error occured while creating.")

    response = client.get(f"/api/object/{key}/{tenant_id}")

    assert response.status_code == 502
    assert response.json() == expected_data
