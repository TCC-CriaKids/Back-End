from fastapi import APIRouter, HTTPException
from models.responsavel import Responsavel
from models.crianca import Crianca
from config.database import colecao_responsaveis, colecao_criancas
from schema.schemas import individual_serial, list_serial
from bson import ObjectId

router = APIRouter()


### RESPONSÁVEL

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

# ROTA QUE DELETA RESPONSÁVEL PELO ID
@router.delete("/deleta-responsavel")
async def deletar_responsavel(id: str):
    resultado = colecao_responsaveis.find_one_and_delete({"_id": ObjectId(id)})
    if not resultado:
        raise HTTPException(status_code=404, detail="Responsável não encontrado para deletar")
    return {
        "mensagem": "Responsável deletado com sucesso"
    }


### CRIANÇA

# ROTA QUE RETORNA TODAS AS CRIANÇAS
@router.get("/todas-criancas")
async def listar_criancas():
    criancas = list_serial(colecao_criancas.find())
    if not criancas:
        raise HTTPException(status_code=404, detail="Não há registros de crianças")
    return criancas

# ROTA QUE RETORNA CRIANÇA PELO ID
@router.get("/buscar-crianca")
async def buscar_crianca(id: str):
    crianca = colecao_criancas.find_one({"_id": ObjectId(id)})
    if not crianca:
        raise HTTPException(status_code=404, detail="Criança não encontrada")
    return individual_serial(crianca)

# ROTA QUE DELETA CRIANÇA PELO ID
@router.delete("/deleta-crianca")
async def deletar_crianca(id: str):
    crianca = colecao_criancas.find_one_and_delete({"_id": ObjectId(id)})
    if not crianca: 
        raise HTTPException(status_code=404, detail="Criança não encontrada para deletar")
    return {
        "mensagem": "Criança deletada com sucesso"
    }