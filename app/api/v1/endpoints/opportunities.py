
from typing import Any, List
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.opportunity import Opportunity
from app.models.client import Client
from app.models.user import User
from app.schemas.opportunity import OpportunityCreate,OpportunityResponse, OpportunityUpdate

from app.api.deps import get_current_user


router = APIRouter()


@router.post(
    "/",
    response_model=OpportunityResponse,
    status_code=status.HTTP_201_CREATED
)
def create_opportunity(
    *,
    db: Session = Depends(get_db),
    opp_in: OpportunityCreate,
    current_user: User = Depends(get_current_user)
) -> Any:

    client = db.query(Client).filter(
        Client.id == opp_in.client_id,
        Client.owner_id == current_user.id
    ).first()

    if not client:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado ou não pertence ao utilizador."
        )

    opportunity = Opportunity(
        **opp_in.model_dump(),
        owner_id=current_user.id
    )

    db.add(opportunity)
    db.commit()
    db.refresh(opportunity)

    return opportunity


@router.get(
    "/",
    response_model=List[OpportunityResponse]
)
def read_opportunities(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
) -> Any:

    return db.query(Opportunity).filter(
        Opportunity.owner_id == current_user.id
    ).offset(skip).limit(limit).all()


@router.put(
    "/{opp_id}",
    response_model=OpportunityResponse
)
def update_opportunity(
    *,
    opp_id: uuid.UUID,
    db: Session = Depends(get_db),
    opp_in: OpportunityUpdate,
    current_user: User = Depends(get_current_user)
) -> Any:

    opportunity = db.query(Opportunity).filter(
        Opportunity.id == opp_id,
        Opportunity.owner_id == current_user.id
    ).first()

    if not opportunity:
        raise HTTPException(
            status_code=404,
            detail="Oportunidade não encontrada."
        )

    update_data = opp_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(opportunity, field, value)

    db.add(opportunity)
    db.commit()
    db.refresh(opportunity)

    return opportunity


@router.delete(
    "/{opp_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_opportunity(
    *,
    opp_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> None:

    opportunity = db.query(Opportunity).filter(
        Opportunity.id == opp_id,
        Opportunity.owner_id == current_user.id
    ).first()

    if not opportunity:
        raise HTTPException(
            status_code=404,
            detail="Oportunidade não encontrada."
        )

    db.delete(opportunity)
    db.commit()

    return None
