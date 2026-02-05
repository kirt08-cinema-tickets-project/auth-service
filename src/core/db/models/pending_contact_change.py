from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, UniqueConstraint, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db.models.base_models import Base
from src.core.db.models.utils import Type

if TYPE_CHECKING:
    from src.core.db.models import UsersORM


class PendingContactChangesORM(Base):
    __tablename__ = "pending_contact_changes"

    id : Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True, index=True)
    type : Mapped[Type]
    value : Mapped[str] = mapped_column(String(256), nullable=False)
    codeHash : Mapped[str] = mapped_column(String(256), nullable=False)
    expiresAt: Mapped[int] = mapped_column(BigInteger, nullable=False)
    account_id : Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    account : Mapped["UsersORM"] = relationship(back_populates="contact_changes")

    __table_args__ = (
        UniqueConstraint("account_id", "type", name="uix_type_account_id"),
    )