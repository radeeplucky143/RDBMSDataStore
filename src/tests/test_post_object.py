import sys
import json
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from os.path import dirname, abspath
from datetime import datetime

sys.path.append(dirname(dirname(abspath(__file__))))

from main import app
from api.models import PostData
client = TestClient(app)


@patch('api.endpoints.DataStore')
def test_post_object_success(mock_data_store):
    """posting record from the database"""

    key = "movie"
    tenant_id = "radeep"
    object = PostData(tenant_id=tenant_id, key=key, data="samjkdhfkjhd", ttl=9)
    expected_data = {'message': f'Dear {object.tenant_id}, Record: {object} insertion Successful.'}

    mock_data_store.return_value.PostData.return_value = True
    mock_data_store.return_value.disconnect.return_value = None
    response = client.post(f"/api/object/", content=json.dumps(object.__dict__))

    assert response.status_code == 201
    assert response.json() == expected_data


@patch('api.endpoints.DataStore')
def test_post_object_record_already_exists(mock_data_store):
    """record already exists"""

    key = "movie"
    tenant_id = "radeep"
    object = PostData(tenant_id=tenant_id, key=key, data="samjkdhfkjhd", ttl=9)
    expected_data = {'message': f"Dear {object.tenant_id}, Record {object} already exists in the database"}

    mock_data_store.return_value.PostData.return_value = f"Record {object} already exists in the database"
    mock_data_store.return_value.disconnect.return_value = None
    response = client.post(f"/api/object/", content=json.dumps(object.__dict__))

    assert response.status_code == 409
    assert response.json() == expected_data



@patch('api.endpoints.DataStore')
def test_post_object_storage_limit_exceeds(mock_data_store):
    """storage_limit exceeds for tenant"""

    key = "movie"
    tenant_id = "radeep"
    object = PostData(tenant_id=tenant_id, key=key, data="samjkdhfkjhd", ttl=9)
    storage_limit = 1000
    storage = 999
    post_data_response = f"Storage limit exceeded. Maximum Storage: {storage_limit}, UsedStorage: {storage}, Available: {storage_limit-storage}, dataSize: {len(object.data)} "
    expected_data = {'message': f"Dear {object.tenant_id}, {post_data_response}"}

    mock_data_store.return_value.PostData.return_value = post_data_response
    mock_data_store.return_value.disconnect.return_value = None
    response = client.post(f"/api/object/", content=json.dumps(object.__dict__))

    assert response.status_code == 409
    assert response.json() == expected_data


@patch('api.endpoints.DataStore')
def test_post_object_exception(mock_data_store):
    """Unexpected Exception"""

    key = "movie"
    tenant_id = "radeep"
    object = PostData(tenant_id=tenant_id, key=key, data="samjkdhfkjhd", ttl=9)
    error = "error occured !!!"
    expected_data = {'error': error}

    mock_data_store.return_value.PostData.side_effect = Exception(error)
    mock_data_store.return_value.disconnect.return_value = None
    response = client.post(f"/api/object/", content=json.dumps(object.__dict__))

    assert response.status_code == 502
    assert response.json() == expected_data
