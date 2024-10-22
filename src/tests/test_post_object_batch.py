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
def test_post_object_batch_success(mock_data_store):
    """posting record from the database"""


    key="sample"
    tenant_id="radeep"
    first = PostData(tenant_id=tenant_id, key=key, data="samjkdhfkjhd", ttl=9)
    second = PostData(tenant_id=tenant_id, key="dummy", data="samjkdhfkjhd", ttl=9)
    objects = [first,first, second, second]
    success = [f'Dear {first.tenant_id}, Record: {first} insertion Successful.']


    second_response = f"Record {first} already exists in the database"
    third_response = f"Storage limit exceeded. Maximum Storage: 1000, UsedStorage: 999, Available: 1, dataSize: 12 "
    failures = [f'Dear {first.tenant_id}, {second_response}', f'Dear {first.tenant_id}, {third_response}']

    expected_data = {'success': success, 'failures': failures, 'exceptions': [f'Error while inserting the record {second}']}
    mock_data_store.return_value.PostData.side_effect = [True, second_response, third_response, Exception("error")]
    mock_data_store.return_value.disconnect.return_value = None
    response = client.post(f"/api/batch/object/", content=json.dumps([object.__dict__ for object in objects]))
    print(response.json())

    assert response.status_code == 200
    assert response.json() == expected_data


@patch('api.endpoints.DataStore')
def test_post_object_batch_exception(mock_data_store):
    """Unexcepted error"""


    key="sample"
    tenant_id="radeep"
    first = PostData(tenant_id=tenant_id, key=key, data="samjkdhfkjhd", ttl=9)
    second = PostData(tenant_id=tenant_id, key="dummy", data="samjkdhfkjhd", ttl=9)
    objects = [first, second]
    error = 'unexpected error'

    expected_data = {'error': error, 'success': [], 'failures': [], 'exceptions': []}
    mock_data_store.side_effect = Exception(error)
    response = client.post(f"/api/batch/object/", content=json.dumps([object.__dict__ for object in objects]))

    assert response.status_code == 502
    assert response.json() == expected_data
