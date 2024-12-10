from typing import Optional

from motor.core import AgnosticDatabase
from pydantic import BaseModel

from src.crud.base import CRUDBase
from src.models.user import User


# ODM, Schema, Schema
class CRUDUser(CRUDBase[User, Optional[BaseModel], Optional[BaseModel]]):
    async def get_by_email(self, db: AgnosticDatabase, *, email: str) -> User | None:  # noqa
        return await self.engine.find_one(User, User.email == email)

    @staticmethod
    def has_password(user: User) -> bool:
        return user.hashed_password is not None

    @staticmethod
    def is_active(user: User) -> bool:
        return user.is_active

    @staticmethod
    def is_superuser(user: User) -> bool:
        return user.is_superuser

    @staticmethod
    def is_email_validated(user: User) -> bool:
        return user.email_validated


user = CRUDUser(User)
