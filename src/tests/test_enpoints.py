import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from src.api.endpoints import router

app = FastAPI()
app.include_router(router)

client = TestClient(app)


def test_get_object_success():
    key = "test_key"
    tenant_id = "test_tenant"
    mock_data = [(1, tenant_id, key, "value", 5, 60, "2024-01-01T00:00:00", "2025-01-01T00:00:00")]

    with patch('src.core.DataStore') as MockDataStore:
        instance = MockDataStore.return_value
        instance.tenantExists.return_value = True
        instance.getKey.return_value = mock_data

        response = client.get(f"/object/{key}/{tenant_id}")
        print(response)

        assert response.status_code == 200
        assert response.json() == {
            "tenant_id": tenant_id,
            "key": key,
            "value": "value",
            "size": 5,
            "ttl": 60,
            "creation_time": "2024-01-01T00:00:00",
            "expiry_time": "2025-01-01T00:00:00"
        }


def test_get_object_key_not_found():
    key = "non_existent_key"
    tenant_id = "test_tenant"

    with patch('src.core.DataStore') as MockDataStore:
        instance = MockDataStore.return_value
        instance.tenantExists.return_value = True
        instance.getKey.return_value = []

        response = client.get(f"/object/{key}/{tenant_id}")

        assert response.status_code == 404
        assert response.json() == {'message': f'Dear {tenant_id},please add Key {key} before requesting.'}


def test_get_object_tenant_not_found():
    key = "test_key"
    tenant_id = "non_existent_tenant"

    with patch('src.core.DataStore') as MockDataStore:
        instance = MockDataStore.return_value
        instance.tenantExists.return_value = False

        response = client.get(f"/object/{key}/{tenant_id}")

        assert response.status_code == 404
        assert response.json() == {'message': f'Dear {tenant_id}, you were not registered/exists in the database.'}


def test_get_object_exception_handling():
    key = "test_key"
    tenant_id = "test_tenant"

    with patch('src.core.DataStore') as MockDataStore:
        instance = MockDataStore.return_value
        instance.tenantExists.side_effect = Exception("Database error")

        response = client.get(f"/object/{key}/{tenant_id}")

        assert response.status_code == 502
        assert response.json() == {'error': 'Database error'}
