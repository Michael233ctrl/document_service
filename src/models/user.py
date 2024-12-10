from pydantic import EmailStr

from src.db.base_class import Base


class User(Base):
    full_name: str
    email: EmailStr
    is_active: bool
    is_superuser: bool