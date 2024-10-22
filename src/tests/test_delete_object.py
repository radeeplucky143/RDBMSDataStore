import sys
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from os.path import dirname, abspath
from datetime import datetime

sys.path.append(dirname(dirname(abspath(__file__))))

from main import app
from api.models import DeleteData
client = TestClient(app)


@patch('api.endpoints.DataStore')
def test_delete_object_success(mock_data_store):
    """successfully deleeting the record from the database"""

    key = "movie"
    tenant_id = "radeep"
    object = DeleteData(tenant_id=tenant_id, key=key)
    expected_data = {'message': f"Dear {tenant_id},Record {object} deleted successfully."}

    mock_data_store.return_value.tenantExists.return_value = True
    mock_data_store.return_value.deleteData.return_value = f"Record {object} deleted successfully."
    mock_data_store.return_value.disconnect.return_value = None
    response = client.delete(f"/api/object/{key}/{tenant_id}")

    assert response.status_code == 200
    assert response.json() == expected_data


@patch('api.endpoints.DataStore')
def test_delete_object_user_not_found(mock_data_store):
    """User Not found case check"""

    key = "movie"
    tenant_id = "shyam"
    expected_data = {'message': f'Dear {tenant_id}, you were not registered/exists in the database.'}

    mock_data_store.return_value.tenantExists.return_value = False
    mock_data_store.return_value.disconnect.return_value = None
    response = client.delete(f"/api/object/{key}/{tenant_id}")

    assert response.status_code == 404
    assert response.json() == expected_data


@patch('api.endpoints.DataStore')
def test_delete_object_record_not_found(mock_data_store):
    """Record not found"""

    key = "movie"
    tenant_id = "radeep"
    object = DeleteData(tenant_id=tenant_id, key=key)
    delete_return = f"Please make sure Record {object} exists in the database before performing delete operation.."
    expected_data = {'message': f"Dear {tenant_id},{delete_return}"}

    mock_data_store.return_value.tenantExists.return_value = True
    mock_data_store.return_value.deleteData.return_value = delete_return
    mock_data_store.return_value.disconnect.return_value = None
    response = client.delete(f"/api/object/{key}/{tenant_id}")

    assert response.status_code == 200
    assert response.json() == expected_data


@patch('api.endpoints.DataStore')
def test_delete_object_Exception(mock_data_store):
    """Unexpected exception case"""

    key = "movie"
    tenant_id = "shyam"
    expected_data = {"error":"error occured"}

    mock_data_store.return_value.tenantExists.side_effect = Exception("error occured")
    response = client.delete(f"/api/object/{key}/{tenant_id}")

    assert response.status_code == 502
    assert response.json() == expected_data


@patch('api.endpoints.DataStore')
def test_delete_expired_Exception(mock_data_store):
    """Unexpected exception case"""

    expected_data = {"error":"error occured"}
    mock_data_store.return_value.deleteExpired.side_effect = Exception("error occured")
    response = client.delete(f"/api/delete/expired")

    assert response.status_code == 502
    assert response.json() == expected_data


@patch('api.endpoints.DataStore')
def test_delete_expired_no_record_found(mock_data_store):
    """NO records found."""

    expected_data = {"message": "No expired records found.."}
    mock_data_store.return_value.deleteExpired.return_value = "No expired records found.."
    mock_data_store.return_value.disconnect.return_value = None
    response = client.delete(f"/api/delete/expired")

    assert response.status_code == 200
    assert response.json() == expected_data


@patch('api.endpoints.DataStore')
def test_delete_expired_records_deleted(mock_data_store):
    """Records deleted."""

    expected_data = {"message": f"Total no of expiry records: 9"}
    mock_data_store.return_value.deleteExpired.return_value = f"Total no of expiry records: 9"
    mock_data_store.return_value.disconnect.return_value = None
    response = client.delete(f"/api/delete/expired")

    assert response.status_code == 200
    assert response.json() == expected_data
