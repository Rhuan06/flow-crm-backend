import uuid
from datetime import datetime, date
from pydantic import BaseModel, Field
from decimal import Decimal
from app.models.opportunity import OpportunityStatus
from typing import Optional
class OpportunityBase(BaseModel):
    title: str = Field(..., min_length=3, description="O título deve ter no mínimo 3 caracteres.")
    description: Optional[str] = None
    value: Decimal =Field(default=0.0, ge=0, description="O valor não pode ser negativo.")
    status: OpportunityStatus = OpportunityStatus.PROSPECTING
    expected_close_date: Optional[date] = None
    client_id: uuid.UUID

class OpportunityCreate(OpportunityBase):
    pass

class OpportunityUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    value: Decimal | None = None
    status: OpportunityStatus | None = None
    expected_close_date: date | None = None
    client_id: uuid.UUID | None = None

class OpportunityResponse(OpportunityBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True