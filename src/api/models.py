from pydantic import BaseModel, Field, validator
from src.api.config import default_ttl
from typing import Any

class PostData(BaseModel):
    tenant_id: str
    key: str = Field(max_length=32)
    data: str
    ttl: int = default_ttl

    @validator('data')
    def check_data_size(cls, v: Any) -> Any:
        max_size_kb = 16*1024
        data_size = len(v.encode('utf-8'))
        if data_size > max_size_kb:
            raise ValueError(f"The 'data' field must not exceed 16 KB. Current size: {data_size} bytes.")
        return v


class GetData(BaseModel):
    key: str
    tenant_id: str


class DeleteData(BaseModel):
    key: str
    tenant_id: str
