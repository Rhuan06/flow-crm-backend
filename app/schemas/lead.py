import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.models.lead import LeadStatus

class LeadBase(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    status: LeadStatus = LeadStatus.NEW

class LeadCreate(LeadBase):
    pass

class LeadUpdate(BaseModel):
    nome: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    status: LeadStatus | None = None

class LeadResponse(LeadBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True