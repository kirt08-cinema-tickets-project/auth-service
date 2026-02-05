from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db.models.base_models import Base

from src.core.db.models.utils import Roles

if TYPE_CHECKING:
    from src.core.db.models import PendingContactChangesORM

class UsersORM(Base):
    __tablename__ = "users"
    id : Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True, index=True)
    phone : Mapped[str] = mapped_column(String(256), nullable=True, unique=True)
    email : Mapped[str] = mapped_column(String(256), nullable=True, unique=True)
    is_phone_verified : Mapped[bool] = mapped_column(default=False)
    is_email_verified : Mapped[bool] = mapped_column(default=False)
    role : Mapped[Roles] = mapped_column(default=Roles.USER)

    contact_changes : Mapped["PendingContactChangesORM"] = relationship(back_populates="account")

