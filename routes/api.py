from fastapi import APIRouter
from . import loginCrianca, loginResponsavel, status, atividades, respostas, responsaveis, criancas, ollama, progresso

# Router principal
api_router = APIRouter()

# Sub-routers
api_router.include_router(status.router, tags=["Status de conexão com o banco"])
api_router.include_router(atividades.router, tags=["Atividades"])
api_router.include_router(respostas.router, tags=["Respostas"])
api_router.include_router(progresso.router, tags=["Progresso"])
api_router.include_router(responsaveis.router, tags=["Responsáveis"])
api_router.include_router(criancas.router, tags=["Crianças"])
api_router.include_router(loginResponsavel.router, tags=["Autenticação - Responsavel"])
api_router.include_router(loginCrianca.router, tags=["Autenticação - Criança"])
api_router.include_router(ollama.router, prefix="/ollama", tags=["Ollama"])