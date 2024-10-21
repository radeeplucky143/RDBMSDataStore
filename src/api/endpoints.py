from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from core.DataStore import DataStore
from api.models import PostData, GetData, DeleteData
import asyncio

router = APIRouter()


@router.get("/object/{key}/{tenant_id}")
async def get_object(key: str, tenant_id: str):
    try:
        datastore = DataStore()
        if datastore.tenantExists(tenant_id):
            data = datastore.getKey(GetData(key=key, tenant_id=tenant_id))
            datastore.disconnect()
            if len(data):
                data = data[0]
                response_data = {
                    "tenant_id": data[1],
                    "key": data[2],
                    "value": data[3],
                    "ttl": data[4],
                    "creation_time": data[5].isoformat(),
                    "expiry_time": data[6].isoformat()
                }
                return JSONResponse(status_code=200, content=response_data)
            message = f'Dear {tenant_id},please add Key {key} before requesting.'
            return JSONResponse(status_code=200, content={'message': message})
        datastore.disconnect()
        return JSONResponse(status_code=200, content={'message': f'Dear {tenant_id}, you were not registered/exists in the database.'})
    except Exception as err:
        return JSONResponse(status_code=502,content={'error': err})


@router.post("/object")
async def post_object(object: PostData):
    try:
        datastore = DataStore()
        if datastore.PostData(object):
            datastore.disconnect()
            return JSONResponse(status_code=201, content={'message': f'Dear {object.tenant_id}, Record: {object} insertion Successful.'})
        datastore.disconnect()
        return JSONResponse(status_code=503, content={'message': f'Dear {object.tenant_id}, Record already exists in database.'})
    except Exception as err:
        datastore.disconnect()
        return JSONResponse(status_code=502, content={'error': str(err)})


@router.post("/batch/object")
async def post_objects(objects: list[PostData]):
    try:
        success = []
        failures = []
        duplicates = []
        datastore = DataStore()
        for object in objects:
            try:
                if datastore.PostData(object):
                    success.append(f'Dear {object.tenant_id}, Record: {object} insertion Successful.')
                else:
                    duplicates.append(f'Dear {object.tenant_id}, Record: {object} already exists in database.')
            except Exception as err:
                failures.append(f'Error while inserting the record {object}')
        datastore.disconnect()
        return JSONResponse(status_code=200, content={'success': success, 'failures': failures, 'duplicates': duplicates})
    except Exception as err:
        return JSONResponse(status_code=502, content={'error': str(err)})


@router.delete("/object/{key}/{tenant_id}")
async def delete_object(key: str, tenant_id: str):
    try:
        datastore = DataStore()
        if datastore.tenantExists(tenant_id):
            data = datastore.deleteData(DeleteData(key=key, tenant_id=tenant_id))
            datastore.disconnect()
            return JSONResponse(status_code=200, content={'message': f'Dear {tenant_id},{data}'})
        datastore.disconnect()
        return JSONResponse(status_code=200, content={'message': f'Dear {tenant_id}, you were not registered/exists in the database.'})
    except Exception as err:
        return JSONResponse(status_code=502, content={'error': err})


@router.delete("/delete/expired")
async def delete_expired():
    try:
        datastore = DataStore()
        response = datastore.deleteExpired()
        datastore.disconnect()
        return JSONResponse(status_code=200, content={'message': response})
    except Exception as err:
        return JSONResponse(status_code=502, content={'error': str(err)})