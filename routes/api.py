from fastapi import APIRouter
from . import login, status, atividades, respostas, responsaveis, criancas, ollama, progresso

# Router principal
api_router = APIRouter()

# Sub-routers
api_router.include_router(status.router, tags=["Status de conexão com o banco"])
api_router.include_router(atividades.router, prefix="/atividades", tags=["Atividades"])
api_router.include_router(respostas.router, prefix="/respostas", tags=["Respostas"])
api_router.include_router(progresso.router, tags=["Progresso"])
api_router.include_router(responsaveis.router, prefix="/responsaveis", tags=["Responsáveis"])
api_router.include_router(criancas.router, prefix="/criancas", tags=["Crianças"])
api_router.include_router(login.router, tags=["Autenticação - Responsavel"])
api_router.include_router(ollama.router, prefix="/ollama", tags=["Ollama"])