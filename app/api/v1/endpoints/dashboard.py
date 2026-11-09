from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.session import get_db

from app.api.deps import get_current_user 
from app.models.user import User
from app.models.client import Client
from app.models.lead import Lead
from app.models.opportunity import Opportunity, OpportunityStatus

router = APIRouter()

@router.get(
    "/summary"
)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # <- Pega quem está logado
):
    
    total_clients = db.query(Client).filter(
        Client.owner_id == current_user.id
    ).count()
    
    
    total_leads = db.query(Lead).filter(
        Lead.owner_id == current_user.id
    ).count()
    
    # Soma apenas os negócios GANHOS deste utilizador
    won_value = db.query(func.sum(Opportunity.value)).filter(
        Opportunity.owner_id == current_user.id,
        Opportunity.status == OpportunityStatus.WON
    ).scalar() or 0.0
    
    # Soma apenas os negócios EM FUNIL deste utilizador
    pipeline_value = db.query(func.sum(Opportunity.value)).filter(
        Opportunity.owner_id == current_user.id,
        Opportunity.status.in_([
            OpportunityStatus.PROSPECTING,
            OpportunityStatus.QUALIFICATION,
            OpportunityStatus.PROPOSAL
        ])
    ).scalar() or 0.0

    return {
        "total_clients": total_clients,
        "total_leads": total_leads,
        "won_value": float(won_value),
        "pipeline_value": float(pipeline_value)
    }