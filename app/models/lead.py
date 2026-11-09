import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import enum

from app.db.session import Base


class LeadStatus(str, enum.Enum):
    NEW = "novo"
    CONTACTED = "contatado"
    QUALIFIED = "qualificado"
    DISQUALIFIED = "desqualificado"
    CONVERTED = "convertido"


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    company: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    source: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    status: Mapped[LeadStatus] = mapped_column(
        SQLEnum(LeadStatus), default=LeadStatus.NEW, nullable=False
    )
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relacionamentos
    owner = relationship("User", back_populates="leads")