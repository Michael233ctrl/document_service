from pydantic import BaseModel, EmailStr, StringConstraints, ConfigDict, field_validator, Field, SecretStr
from odmantic import ObjectId


class UserLogin(BaseModel):
    username: str
    password: str


class UserBase(BaseModel):
    email: EmailStr
    is_active: bool
    is_superuser: bool
    full_name: str


class UserInDBBase(UserBase):
    id: ObjectId
    model_config = ConfigDict(from_attributes=True)


# Additional properties to return via API
class User(UserInDBBase):
    model_config = ConfigDict(populate_by_name=True)
