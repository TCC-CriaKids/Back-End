from fastapi import FastAPI  # Importa a classe FastAPI
# from routes.route import router  # Importa as rotas definidas em route.py
from routes import atividades, respostas

app = FastAPI()  # Cria a aplicação FastAPI

# app.include_router(router)  # Inclui as rotas no aplicativo
app.include_router(atividades.router, prefix="/atividades", tags=["atividades"])
app.include_router(respostas.router, prefix="/respostas", tags=["respostas"])
