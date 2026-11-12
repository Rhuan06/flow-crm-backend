from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.user import (
    UserCreate,
    UserResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from app.schemas.token import Token
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_password_reset_token,
    verify_password_reset_token,
)
from app.api.deps import get_current_user

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
@limiter.limit("5/minute")
def register_user(
    request: Request,
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate
) -> Any:
    """Registra um novo usuário no sistema."""
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um usuário com este email."
        )

    db_user = User(
        name=user_in.name,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        role=UserRole.SELLER
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post(
    "/login",
    response_model=Token,
)
@limiter.limit("5/minute")
def login_access_token(
    request: Request,
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """Autentica o usuário e retorna um token de acesso."""
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

    return {
        "access_token": create_access_token(subject=user.id),
        "token_type": "bearer"
    }


@router.get(
    "/me",
    response_model=UserResponse,
)
def read_users_me(
    current_user: User = Depends(get_current_user),
) -> Any:
    """Retorna os dados do usuário atualmente autenticado."""
    return current_user


@router.post("/forgot-password")
@limiter.limit("3/minute")
def forgot_password(
    request: Request,
    body: ForgotPasswordRequest,
    db: Session = Depends(get_db),
) -> Any:
    """Gera um link de recuperação de senha (expira em 15 minutos)."""
    user = db.query(User).filter(User.email == body.email).first()

    if user and user.is_active:
        reset_token = create_password_reset_token(email=user.email)
        reset_link = f"http://localhost:3000/reset-password?token={reset_token}"
        # Em desenvolvimento, exibe o link no terminal do backend
        print(f"\n[FLOWCRM - RECUPERAÇÃO DE SENHA] Link para {user.email}:\n{reset_link}\n")

    # Resposta idêntica existindo ou não o e-mail (proteção contra enumeração de usuários)
    return {
        "message": "Se o e-mail estiver cadastrado, enviaremos as instruções de recuperação."
    }


@router.post("/reset-password")
@limiter.limit("5/minute")
def reset_password(
    request: Request,
    body: ResetPasswordRequest,
    db: Session = Depends(get_db),
) -> Any:
    """Valida o token temporário e atualiza a senha do usuário."""
    email = verify_password_reset_token(body.token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido ou expirado. Solicite uma nova recuperação.",
        )

    user = db.query(User).filter(User.email == email).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado ou inativo.",
        )

    if len(body.new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A nova senha deve ter no mínimo 6 caracteres.",
        )

    user.hashed_password = get_password_hash(body.new_password)
    db.commit()

    return {"message": "Senha redefinida com sucesso."}