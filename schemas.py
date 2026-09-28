from datetime import date

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ProfileCreate(BaseModel):
    phone: str | None = None
    address: str | None = None
    date_of_birth: date | None = None
    bio: str | None = None

class ProfileUpdate(BaseModel):
    phone: str | None = None
    address: str | None = None
    date_of_birth: date | None = None
    bio: str | None = None