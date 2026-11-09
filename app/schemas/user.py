import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.models.user import UserRole

# Schema base com campos comuns de utilizador
class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole = UserRole.SELLER


# Schema para recepção de dados no Cadastro (Exige a senha)
class UserCreate(UserBase):
    password: str


# Schema de resposta (NUNCA devolve o hashed_password por segurança)
class UserResponse(UserBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Permite mapeamento direto a partir do SQLAlchemy