from fastapi import FastAPI  # Importa a classe FastAPI
# from routes.route import router  # Importa as rotas definidas em route.py
from routes import atividades, respostas, cadastro

app = FastAPI()  # Cria a aplicação FastAPI

# app.include_router(router)  # Inclui as rotas no aplicativo
app.include_router(atividades.router, tags=["atividades"])
app.include_router(respostas.router, tags=["respostas"])
app.include_router(cadastro.router, tags=["cadastro"])
