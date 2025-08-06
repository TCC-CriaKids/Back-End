from fastapi import APIRouter, HTTPException
from models.responsavel import Responsavel
from models.crianca import Crianca
from config.database import colecao_responsaveis, colecao_criancas
from schema.schemas import individual_serial, list_serial
from bson import ObjectId

router = APIRouter()

# ROTA QUE RETORNA TODOS OS RESPONSAVEIS
@router.get("/todos-responsaveis")
async def listar_responsaveis():
    responsaveis = list_serial(colecao_responsaveis.find())
    if not responsaveis:
        raise HTTPException(status_code=404, detail="Não há registros de responsáveis")
    return responsaveis

# ROTA QUE RETORNA RESPONSAVEL PELO ID
@router.get("/buscar-responsavel")
async def buscar_responsavel(id: str):
    responsavel = colecao_responsaveis.find_one({"_id": ObjectId(id)})
    if not responsavel:
        raise HTTPException(status_code=404, detail="Responsável não encontrado")
    return individual_serial(responsavel)