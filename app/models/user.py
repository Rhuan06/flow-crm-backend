import uuid
from datetime import datetime, timezone
import enum
from sqlalchemy import String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.session import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "gerente"
    SELLER = "vendedor"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(150), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole), default=UserRole.SELLER, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relacionamentos ativos
    clients = relationship("Client", back_populates="owner")
    leads = relationship("Lead", back_populates="owner")

    
    opportunities = relationship("Opportunity", back_populates="owner")
    # tasks = relationship("Task", back_populates="owner")