from fastapi import APIRouter, HTTPException
from config.database import colecao_responsaveis
from schema.schemas import individual_serial
from pydantic import BaseModel
import bcrypt

router = APIRouter()

class LoginResponsavel(BaseModel):
    email: str
    senha: str

@router.post("/login")
async def login(dados: LoginResponsavel):  
    responsavel = colecao_responsaveis.find_one({"email": dados.email})
    if not responsavel:
        raise HTTPException(status_code=400, detail="Email ou senha incorretos")

    if not bcrypt.checkpw(dados.senha.encode('utf-8'), responsavel['senha'].encode('utf-8')):
        raise HTTPException(status_code=400, detail="Email ou senha incorretos")

    # Remove a senha antes de retornar
    responsavel.pop("senha", None)
    dados_serializados = individual_serial(responsavel)

    return {
        "mensagem": "Login realizado com sucesso",
        "dados": dados_serializados
    }