# routes/progresso.py
from fastapi import APIRouter, HTTPException, Depends, Path
from models.Progresso import Progresso
from config.database import colecao_progresso, colecao_atividades
from schema.schemas import individual_serial, list_serial
from bson import ObjectId
from datetime import datetime

router = APIRouter()

# ROTA QUE RETORNA TODO O PROGRESSO DE UMA CRIANÇA
@router.get("/progresso/{crianca_id}")
async def listar_progresso(crianca_id: str = Path(..., description="ID da criança")):
    progresso = list_serial(colecao_progresso.find({"crianca_id": crianca_id}))
    return progresso

# ROTA QUE RETORNA PROGRESSO POR NÍVEL
@router.get("/progresso/{crianca_id}/nivel/{nivel}")
async def progresso_por_nivel(crianca_id: str, nivel: int):
    progresso = list_serial(
        colecao_progresso.find({"crianca_id": crianca_id, "nivel": nivel})
    )
    return progresso

@router.get("/progresso/{crianca_id}/ultimas/{quantidade}")
async def ultimas_atividades(crianca_id: str, quantidade: int = 5):
    progresso = list_serial(
        colecao_progresso.find({"crianca_id": crianca_id}).sort("data", -1).limit(quantidade)
    )
    
    if not progresso:
        raise HTTPException(status_code=404, detail="Nenhum progresso encontrado para esta criança")
    
    # Pode retornar só o que interessa: atividade, resultado e tentativas
    resultado = [
        {
            "atividade_id": p["atividade_id"],
            "resultado": p["resultado"],
            "tentativas": p["tentativas"]
        } for p in progresso
    ]
    
    return resultado

# ROTA QUE DELETA PROGRESSO PELO ID
@router.delete("/progresso/{id}")
async def deletar_progresso(id: str = Path(..., description="ID do progresso")):
    resultado = colecao_progresso.find_one_and_delete({"_id": ObjectId(id)})
    if not resultado:
        raise HTTPException(status_code=404, detail="Progresso não encontrado")
    return {"mensagem": "Progresso deletado com sucesso"}
