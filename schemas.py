from typing import List, Optional

from pydantic import BaseModel, EmailStr, constr, root_validator, validator


class SuccessResponse(BaseModel):
    message: str


class User(BaseModel):
    id: Optional[int]
    username: Optional[str]
    telegram_id: Optional[int]

    class Config:
        orm_mode = True


class Wallet(BaseModel):
    id: Optional[int]
    user_id: Optional[int]
    balance: Optional[int]

    class Config:
        orm_mode = True
