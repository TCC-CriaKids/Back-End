from fastapi import APIRouter, HTTPException
from config.database import colecao_criancas
from schema.schemas import individual_serial
from pydantic import BaseModel
import bcrypt

router = APIRouter()

class LoginCrianca(BaseModel):
    cpf: str
    senha: str

@router.post("/login_crianca")
async def login_crianca(dados: LoginCrianca):  
    if not dados.cpf or not dados.senha:
        raise HTTPException(status_code=400, detail="CPF ou senha não informados")

    crianca = colecao_criancas.find_one({"cpf": dados.cpf})
    if not crianca:
        raise HTTPException(status_code=400, detail="CPF ou senha incorretos")

    if not bcrypt.checkpw(dados.senha.encode('utf-8'), crianca['senha'].encode('utf-8')):
        raise HTTPException(status_code=400, detail="CPF ou senha incorretos")

    crianca.pop("senha", None)
    dados_serializados = individual_serial(crianca)

    return {
        "mensagem": "Login realizado com sucesso",
        "dados": dados_serializados
    }