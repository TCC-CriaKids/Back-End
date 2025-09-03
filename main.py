from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.api import api_router

app = FastAPI(title="CRIA Kids")

# 🔥 Habilitar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, troque "*" pelo domínio do seu front
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas com prefixo /api
app.include_router(api_router, prefix="/api")
