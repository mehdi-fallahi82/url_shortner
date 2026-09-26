from pydantic import HttpUrl , BaseModel
from datetime import datetime

class url_create(BaseModel):
    url : HttpUrl

class url_response(BaseModel):
        id: int
        original_url: str
        short_code: str
        short_url: str
        clicks: int
        created_at: datetime

class config:
    from_attribute = True