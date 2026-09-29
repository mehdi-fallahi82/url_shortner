from datetime import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl, EmailStr, Field


class user_create_account(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=6)


class user_response(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class url_create(BaseModel):
    original_url: str
    custom_code: Optional[str] = None

class url_response(BaseModel):
    id: int
    original_url: str
    short_code: str
    short_url: str
    clicks: int
    created_at: datetime

    class Config:
        from_attributes = True


class token(BaseModel):
    access_token: str
    token_type: str
