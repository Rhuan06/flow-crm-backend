import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr


class ClientBase(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None

# schema para resposta de cliente, incluindo campos adicionais como id, owner_id e created_at
class ClientResponse(ClientBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True


