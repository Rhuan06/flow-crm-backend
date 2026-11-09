from typing import Any, List
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.client import Client
from app.models.user import User
from app.schemas.client import ClientCreate, ClientResponse, ClientUpdate
from app.api.deps import get_current_user

router = APIRouter()

@router.post(
    "/",
    response_model=ClientResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_client(
    *,
    db: Session = Depends(get_db),
    client_in: ClientCreate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """ Cria um novo usuário associado ao usuário atual."""
    client = Client(
        name=client_in.name,
        email=client_in.email,
        phone=client_in.phone,
        owner_id=current_user.id
    )

    db.add(client)
    db.commit()
    db.refresh(client)

    return client

@router.get(
    "/",
    response_model=List[ClientResponse]
)
def read_clients(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
) -> Any:
    """Retorna todos os clientes associados ao usuário atual"""
    clients = db.query(Client).filter(
        Client.owner_id == current_user.id
    ).offset(skip).limit(limit).all()
    return clients

@router.get(
    "/{client_id}",
    response_model=ClientResponse
)
def read_client_by_id(
    client_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """Retorna um cliente específico pelo ID, se ele pertencer ao usuário atual"""
    client = db.query(Client).filter(
        Client.id == client_id,
        Client.owner_id == current_user.id
    ).first()

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client não encontrado."
        )

    return client

@router.put(
    "/{client_id}",
    response_model=ClientResponse
)
def update_client(
    *,
    client_id: uuid.UUID,
    db: Session = Depends(get_db),
    client_in: ClientUpdate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """Atualiza os dados de um cliente existente, pertencente ao usuário atual"""
    client = db.query(Client).filter(
        Client.id == client_id,
        Client.owner_id == current_user.id
    ).first()

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado."
        )

    update_data = client_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(client, field, value)

    db.add(client)
    db.commit()
    db.refresh(client)
    return client

@router.delete(
    "/{client_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_client(
    *,
    client_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> None:
    client = db.query(Client).filter(
        Client.id == client_id,
        Client.owner_id == current_user.id
    ).first()

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado."
        )

    db.delete(client)
    db.commit()
    return None