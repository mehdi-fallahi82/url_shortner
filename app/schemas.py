from datetime import datetime
from pydantic import BaseModel, HttpUrl


class url_create(BaseModel):
    url: HttpUrl


class url_response(BaseModel):
    id: int
    original_url: str
    short_code: str
    short_url: str
    clicks: int
    created_at: datetime

    class Config:
        from_attributes = True