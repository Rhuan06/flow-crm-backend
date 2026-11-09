from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token
from app.core.security import get_password_hash, verify_password, create_access_token
from app.api.deps import get_current_user

router = APIRouter()

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)

def register_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate
) -> Any:
    """Registra um novo usuário no sistema."""
    # Verifia se já existe um ultilizador com o mesmo email
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um usuário com este email."
        )

    # Cria um novo usuário, aplicando o hash da senha
    db_user = User(
        name=user_in.name,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role
    )

    # Adiciona o usuário ao banco de dados
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.post(
    "/login",
    response_model=Token,
)
def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """Autentica o usuário e retorna um token de acesso."""
    # Busca o usuário pelo email fornecido (que é o username no OAuth2PasswordRequestForm)
    user = db.query(User).filter(
        User.email == form_data.username
    ).first()
    if not user or not verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo.",
        )

    # Gera e retorna o token de acesso
    return {
        "access_token": create_access_token(subject=user.id),
        "token_type": "bearer"
    }


@router.get(
    "/me",
    response_model=UserResponse,
)
def read_users_me(
    current_user: User = Depends (get_current_user),
) -> Any:
    """Retorna os dados do usuário atualmente autenticado."""
    return current_user
