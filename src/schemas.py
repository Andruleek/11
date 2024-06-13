from datetime import datetime, date
from pydantic import BaseModel, EmailStr

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: date | None = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass

class ContactInDB(ContactBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token : str
    refresh_token: str
    token_type   : str = "bearer"
class UserResponse(BaseModel):
    id      : int
    username: str
    email   : str
    class Config:
        orm_mode = True