from pydantic import BaseModel

#Schema da resposta do endpoint de login(Retorno do token)
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

#Schema do Payload do token JWT
class TokenData(BaseModel):
    sub: str | None = None