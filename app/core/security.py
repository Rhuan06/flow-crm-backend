
from datetime import datetime, timedelta, timezone
from typing import Any, Union

import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from app.core.config import settings


# Configuração do hash de senhas utilizando Argon2
pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],
    deprecated="auto"
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha corresponde ao hash armazenado."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Gera um hash seguro para a senha."""
    return pwd_context.hash(password)


def create_access_token(
    subject: Union[str, Any],
    expires_delta: timedelta | None = None
) -> str:
    """Cria um token JWT de acesso."""

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "scope": "access"
    }

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def create_password_reset_token(email: str) -> str:
    """Cria um token JWT exclusivo para recuperação de senha."""

    expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode = {
        "exp": expire,
        "sub": email,
        "scope": "password_reset"
    }

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def verify_password_reset_token(token: str) -> str | None:
    """Valida o token de recuperação e retorna o e-mail."""

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        if payload.get("scope") != "password_reset":
            return None

        return payload.get("sub")

    except InvalidTokenError:
        return None
