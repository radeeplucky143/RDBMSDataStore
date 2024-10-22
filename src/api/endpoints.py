from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from core.DataStore import DataStore
from api.models import PostData, GetData, DeleteData

router = APIRouter()


@router.get("/object/{key}/{tenant_id}")
def get_object(key: str, tenant_id: str):
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
                    "size": data[4],
                    "ttl": data[5],
                    "creation_time": data[6].isoformat(),
                    "expiry_time": data[7].isoformat()
                }
                return JSONResponse(status_code=200, content=response_data)
            return JSONResponse(status_code=404, content={'message': f'Dear {tenant_id},please add Key {key} before requesting.'})
        datastore.disconnect()
        return JSONResponse(status_code=404, content={'message': f'Dear {tenant_id}, you were not registered/exists in the database.'})
    except Exception as err:
        return JSONResponse(status_code=502,content={'error': str(err)})


@router.post("/object")
def post_object(object: PostData):
    try:
        datastore = DataStore()
        status = datastore.PostData(object)
        if status == True:
            datastore.disconnect()
            return JSONResponse(status_code=201, content={'message': f'Dear {object.tenant_id}, Record: {object} insertion Successful.'})
        datastore.disconnect()
        return JSONResponse(status_code=409, content={'message': f'Dear {object.tenant_id}, {status}'})
    except Exception as err:
        datastore.disconnect()
        return JSONResponse(status_code=502, content={'error': str(err)})


@router.post("/batch/object")
def post_objects(objects: list[PostData]):
    try:
        success = []
        failures = []
        exceptions = []
        datastore = DataStore()
        for object in objects:
            try:
                status = datastore.PostData(object)
                if status == True:
                    success.append(f'Dear {object.tenant_id}, Record: {object} insertion Successful.')
                else:
                    failures.append(f'Dear {object.tenant_id}, {status}')
            except Exception as err:
                exceptions.append(f'Error while inserting the record {object}')
        datastore.disconnect()
        return JSONResponse(status_code=200, content={'success': success, 'failures': failures, 'exceptions': exceptions})
    except Exception as err:
        return JSONResponse(status_code=502, content={'error': str(err), 'success': success, 'failures': failures, 'exceptions': exceptions})


@router.delete("/object/{key}/{tenant_id}")
def delete_object(key: str, tenant_id: str):
    try:
        datastore = DataStore()
        if datastore.tenantExists(tenant_id):
            data = datastore.deleteData(DeleteData(key=key, tenant_id=tenant_id))
            datastore.disconnect()
            return JSONResponse(status_code=200, content={'message': f'Dear {tenant_id},{data}'})
        datastore.disconnect()
        return JSONResponse(status_code=404, content={'message': f'Dear {tenant_id}, you were not registered/exists in the database.'})
    except Exception as err:
        return JSONResponse(status_code=502, content={'error': str(err)})


@router.delete("/delete/expired")
def delete_expired():
    try:
        datastore = DataStore()
        response = datastore.deleteExpired()
        datastore.disconnect()
        return JSONResponse(status_code=200, content={'message': response})
    except Exception as err:
        return JSONResponse(status_code=502, content={'error': str(err)})
