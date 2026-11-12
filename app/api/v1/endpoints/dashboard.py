from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.client import Client
from app.models.lead import Lead
from app.models.opportunity import Opportunity, OpportunityStatus
from app.schemas.dashboard import DashboardSummary

router = APIRouter()


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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

    # Agrupamento de oportunidades por etapa do funil
    stage_counts_query = (
        db.query(Opportunity.status, func.count(Opportunity.id))
        .filter(Opportunity.owner_id == current_user.id)
        .group_by(Opportunity.status)
        .all()
    )

    counts_map = {
        (status.value if hasattr(status, "value") else str(status)): count
        for status, count in stage_counts_query
    }

    # Garante que todas as etapas do Enum apareçam no gráfico (mesmo com 0)
    opportunities_by_stage = [
        {
            "stage": status.value,
            "count": counts_map.get(status.value, 0)
        }
        for status in OpportunityStatus
    ]

    # Cálculo da Taxa de Conversão (% de negócios ganhos sobre o total)
    total_opportunities = sum(counts_map.values())
    won_count = counts_map.get(OpportunityStatus.WON.value, 0)
    conversion_rate = (
        round((won_count / total_opportunities) * 100, 1)
        if total_opportunities > 0
        else 0.0
    )

    return {
        "total_clients": total_clients,
        "total_leads": total_leads,
        "won_value": float(won_value),
        "pipeline_value": float(pipeline_value),
        "conversion_rate": conversion_rate,
        "opportunities_by_stage": opportunities_by_stage
    }