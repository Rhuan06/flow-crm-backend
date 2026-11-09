import uuid
from datetime import datetime, date
from pydantic import BaseModel
from decimal import Decimal
from app.models.opportunity import OpportunityStatus

class OpportunityBase(BaseModel):
    title: str
    description: str | None = None
    value: Decimal | None = None
    status: OpportunityStatus = OpportunityStatus.PROSPECTING
    expected_close_date: date | None = None
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