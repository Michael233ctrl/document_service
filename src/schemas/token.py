from pydantic import BaseModel
from odmantic import ObjectId



class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str


class TokenPayload(BaseModel):
    sub: ObjectId | None = None
    refresh: bool | None = False
    totp: bool | None = False
