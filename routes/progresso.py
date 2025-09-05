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

# ROTA DE TESTE: criação manual de progresso
# No uso normal, o progresso é gerado automaticamente ao responder atividades
# @router.post("/progresso")
# async def adicionar_progresso(progresso: Progresso):
#     # Preenche a data se não vier
#     if not progresso.data:
#         progresso.data = datetime.utcnow()
    
#     resultado = colecao_progresso.insert_one(progresso.model_dump())
#     return {
#         "id": str(resultado.inserted_id),
#         "mensagem": "Progresso registrado com sucesso!"
#     }

# ROTA QUE DELETA PROGRESSO PELO ID
@router.delete("/progresso/{id}")
async def deletar_progresso(id: str = Path(..., description="ID do progresso")):
    resultado = colecao_progresso.find_one_and_delete({"_id": ObjectId(id)})
    if not resultado:
        raise HTTPException(status_code=404, detail="Progresso não encontrado")
    return {"mensagem": "Progresso deletado com sucesso"}
