from typing import Any, List
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.lead import Lead
from app.models.user import User
from app.schemas.lead import LeadCreate, LeadResponse, LeadUpdate
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
def create_lead(
    *,
    db: Session = Depends(get_db),
    lead_in: LeadCreate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """Cria um novo lead associado ao utilizador autenticado."""
    lead = Lead(
        name=lead_in.name,
        email=lead_in.email,
        phone=lead_in.phone,
        status=lead_in.status,
        owner_id=current_user.id
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead

@router.get(
    "/", 
    response_model=List[LeadResponse]
)
def read_leads(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
) -> Any:
    """Lista todos os leads do utilizador autenticado."""
    return db.query(Lead).filter(
        Lead.owner_id == current_user.id
    ).offset(skip).limit(limit).all()

@router.put(
    "/{lead_id}",
    response_model=LeadResponse
)
def update_lead(
    *,
    lead_id: uuid.UUID,
    db: Session = Depends(get_db),
    lead_in: LeadUpdate,
    current_user: User = Depends(get_current_user)
) -> Any:
    lead = db.query(Lead).filter(
        Lead.id == lead_id, 
        Lead.owner_id == current_user.id
    ).first()
    
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Lead não encontrado."
        )
    
    update_data = lead_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(lead, field, value)
        
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead

@router.delete(
    "/{lead_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_lead(
    *,
    lead_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> None:
    lead = db.query(Lead).filter(
        Lead.id == lead_id, 
        Lead.owner_id == current_user.id
    ).first()
    
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Lead não encontrado."
        )
        
    db.delete(lead)
    db.commit()
    return None