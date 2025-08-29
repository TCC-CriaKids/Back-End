from fastapi import APIRouter, HTTPException
from config.database import colecao_responsaveis
from schema.schemas import individual_serial
import bcrypt

router = APIRouter()

@router.post("/login")
async def login(email: str, senha: str):
    responsavel = colecao_responsaveis.find_one({"email": email})
    if not responsavel:
        raise HTTPException(status_code=400, detail="Email ou senha incorretos")

    if not bcrypt.checkpw(senha.encode('utf-8'), responsavel['senha'].encode('utf-8')):
        raise HTTPException(status_code=400, detail="Email ou senha incorretos")

    # Remove a senha antes de retornar
    responsavel.pop("senha", None)
    dados_serializados = individual_serial(responsavel)

    return {
        "mensagem": "Login realizado com sucesso",
        "dados": dados_serializados
    }