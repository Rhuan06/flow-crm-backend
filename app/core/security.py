from datetime import datetime, timedelta, timezone
from typing import Any, Union
import jwt
from passlib.context import CryptContext

from app.core.config import settings

# Configuração do contexto de hash utilizando Argon2
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    #Verifica se a senha fornecida em texto limpo corresponde ao hash guardado.
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    #gera o hash seguro da senha
    return pwd_context.hash(password)

def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """
    Cria um Token de Acesso JWT assinado.
    :param subject: Identificador do utilizador (geralmente o ID ou E-mail).
    :param expires_delta: Tempo de expiração personalizado do token.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    #Payload com os dados salvos dentro do token
    to_encode = {
        "exp": expire,          # Data/hora de expiração
        "sub": str(subject)     # Assunto/ID do utilizador
    }

    # Assina o token usando a SECRET_KEY e o ALGORITHM definidos no .env
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt