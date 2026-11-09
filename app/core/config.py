# app/core/config.py

# No Pydantic v2, o BaseSettings deve ser importado de 'pydantic_settings'
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Configurações gerais da aplicação
    PROJECT_NAME: str = "FlowCRM"
    API_V1_STR: str = "/api/v1"
    
    # Chave secreta para assinatura dos tokens JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    # String de conexão do PostgreSQL
    DATABASE_URL: str

    # Instrução para ler automaticamente as variáveis do arquivo .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


# Instância global para carregar as configurações ao iniciar a aplicação
settings = Settings()