from pydantic import BaseModel, EmailStr, ConfigDict, Field

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    model_config = ConfigDict(from_attributes=True)
