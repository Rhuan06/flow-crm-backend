from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.endpoints import auth
from fastapi.responses import JSONResponse
from app.api.v1.endpoints import auth, clients, leads, opportunities, dashboard

app = FastAPI(
    title="FlowCRM API",
    description="API para o sistema de gestaão de clientes e vendas FlowCRM",
    version='1.0.0'
)

@app.get("/", tags=["Health Check"])
def read_root():
    return JSONResponse(
        content={
            "message": "Bem-vindo á API do FlowCRM! O sistema está online."
        }
    )

@app.get("/api/v1/health", tags=["Health Check"])
def health_check():
    return JSONResponse(
        content={
            "status": "ok",
            "environment": "development",
        }
    )


app.include_router(
    auth.router, 
    prefix=f"{settings.API_V1_STR}/auth", 
    tags=["Autenticação"]
)



app.include_router(
    clients.router, 
    prefix=f"{settings.API_V1_STR}/clients", 
    tags=["Clientes"]
)

app.include_router(
    leads.router, 
    prefix=f"{settings.API_V1_STR}/leads", 
    tags=["Leads"]
)

app.include_router(
    opportunities.router, 
    prefix=f"{settings.API_V1_STR}/opportunities", 
    tags=["Oportunidades"]
)

app.include_router(
    dashboard.router,
    prefix=f"{settings.API_V1_STR}/dashboard",
    tags=["Dashboard"]
)