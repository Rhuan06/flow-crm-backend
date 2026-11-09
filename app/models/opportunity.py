import uuid
from datetime import datetime, timezone, date
import enum
from sqlalchemy import String, Text, Numeric, Date, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from decimal import Decimal


from app.db.session import Base

class OpportunityStatus(str, enum.Enum):
    PROSPECTING = "prospeccao"
    QUALIFICATION = "qualificacao"
    PROPOSAL = "proposta"
    WON = "ganho"
    LOST = "perdido"


class Opportunity(Base):
    __tablename__ = "opportunities"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    value: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=True
    )

    status: Mapped[OpportunityStatus] = mapped_column(
        SQLEnum(OpportunityStatus),
        default=OpportunityStatus.PROSPECTING,
        nullable=False
    )

    expected_close_date: Mapped[date] = mapped_column(
        Date,
        nullable=True
    )

    client_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("clientes.id"),
        nullable=False
    )

    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    client = relationship(
        "Client",
        back_populates="opportunities"
    )

    owner = relationship(
        "User",
        back_populates="opportunities"
    )
