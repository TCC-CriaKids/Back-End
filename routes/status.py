from fastapi import APIRouter, HTTPException
from config.database import colecao_responsaveis, colecao_criancas

router = APIRouter()

@router.get("/")
async def status_banco():
    try:
        # consulta rápida só pra testar conexão
        colecao_responsaveis.find_one()
        colecao_criancas.find_one()
        return {"status": "ok", "mensagem": "Conectado com o banco de dados"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao conectar ao banco: {e}")
