from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


from src.core.db.models import Base

class UsersORM(Base):
    __tablename__ = "users"
    id : Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True, index=True)
    phone : Mapped[str] = mapped_column(String(256), nullable=True, unique=True)
    email : Mapped[str] = mapped_column(String(256), nullable=True, unique=True)
    is_phone_verified : Mapped[bool] = mapped_column(default=False)
    is_email_verified : Mapped[bool] = mapped_column(default=False)
