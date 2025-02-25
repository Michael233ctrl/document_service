from pydantic import (
    BaseModel,
    EmailStr,
    ConfigDict,
)
from odmantic import ObjectId


class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserInDBBase(UserBase):
    id: ObjectId
    model_config = ConfigDict(from_attributes=True)


# Additional properties to return via API
class User(UserInDBBase):
    model_config = ConfigDict(populate_by_name=True)
