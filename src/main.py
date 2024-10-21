from fastapi import FastAPI
from api.endpoints import router

app = FastAPI(title="RDBMS KeyValue DataStore", description="RDBMS DataStore supports CRD operations.")
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8083, reload=True)
