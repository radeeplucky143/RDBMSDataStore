import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from api.endpoints import router

client = TestClient(router)

mock_data = {
    "tenant_id": "tenant123",
    "key": "test_key",
    "value": "test_value",
    "ttl": 3600,
    "creation_time": "2024-10-19T12:34:56",
    "expiry_time": "2024-10-20T12:34:56"
}


@patch("core.DataStore")
def test_get_object(mock_datastore):
    mock_instance = mock_datastore.return_value
    mock_instance.tenantExists.return_value = True
    mock_instance.getKey.return_value = [(1, "tenant123", "test_key", "test_value", 3600, mock_data["creation_time"], mock_data["expiry_time"])]

    response = client.get("/object/test_key/tenant123")

    assert response.status_code == 200
    assert response.json() == {
        "tenant_id": "tenant123",
        "key": "test_key",
        "value": "test_value",
        "ttl": 3600,
        "creation_time": "2024-10-19T12:34:56",
        "expiry_time": "2024-10-20T12:34:56"
    }
    mock_instance.disconnect.assert_called_once()


@patch("core.DataStore")
def test_post_object(mock_datastore):
    mock_instance = mock_datastore.return_value
    mock_instance.PostData.return_value = True

    post_data = {
        "tenant_id": "tenant123",
        "key": "test_key",
        "value": "test_value",
        "ttl": 3600
    }

    response = client.post("/object", json=post_data)

    assert response.status_code == 201
    assert response.json() == {
        "message": "Dear tenant123, Record: PostData(tenant_id='tenant123', key='test_key', value='test_value', ttl=3600) insertion Successful."
    }
    mock_instance.disconnect.assert_called_once()


@patch("core.DataStore")
def test_post_objects(mock_datastore):
    mock_instance = mock_datastore.return_value
    mock_instance.PostData.side_effect = [True, False]

    post_data = [
        {"tenant_id": "tenant123", "key": "key1", "value": "value1", "ttl": 3600},
        {"tenant_id": "tenant124", "key": "key2", "value": "value2", "ttl": 7200},
    ]

    response = client.post("/batch/object", json=post_data)

    assert response.status_code == 200
    assert response.json() == {
        "success": ["Dear tenant123, Record: PostData(tenant_id='tenant123', key='key1', value='value1', ttl=3600) insertion Successful."],
        "failures": [],
        "duplicates": ["Dear tenant124, Record: PostData(tenant_id='tenant124', key='key2', value='value2', ttl=7200) already exists in database."]
    }
    mock_instance.disconnect.assert_called_once()


@patch("core.DataStore")
def test_delete_object(mock_datastore):
    mock_instance = mock_datastore.return_value
    mock_instance.tenantExists.return_value = True
    mock_instance.deleteData.return_value = "Record deletion successful"

    response = client.delete("/object/test_key/tenant123")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Dear tenant123,Record deletion successful"
    }
    mock_instance.disconnect.assert_called_once()


@patch("core.DataStore")
def test_delete_expired(mock_datastore):
    mock_instance = mock_datastore.return_value
    mock_instance.deleteExpired.return_value = "Deleted expired records"

    response = client.delete("/delete/expired")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Deleted expired records"
    }
    mock_instance.disconnect.assert_called_once()


# Exception handling tests

@patch("core.DataStore")
def test_get_object_throws_exception(mock_datastore):
    mock_instance = mock_datastore.return_value
    mock_instance.tenantExists.side_effect = Exception("Database error")

    response = client.get("/object/test_key/tenant123")

    assert response.status_code == 502
    assert response.json() == {"error": "Database error"}


@patch("core.DataStore")
def test_post_object_throws_exception(mock_datastore):
    mock_instance = mock_datastore.return_value
    mock_instance.PostData.side_effect = Exception("Database error")

    post_data = {
        "tenant_id": "tenant123",
        "key": "test_key",
        "value": "test_value",
        "ttl": 3600
    }

    response = client.post("/object", json=post_data)

    assert response.status_code == 502
    assert response.json() == {"error": "Database error"}
    mock_instance.disconnect.assert_called_once()

test_post_object_throws_exception(mock_data)
