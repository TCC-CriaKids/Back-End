from fastapi import FastAPI  # Importa a classe FastAPI
from routes.api import api_router

app = FastAPI(title="CRIA Kids")  # Cria a aplicação FastAPI

app.include_router(api_router, prefix="/api")