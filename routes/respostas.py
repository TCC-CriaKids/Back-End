from fastapi import APIRouter, HTTPException, Depends, Path
from models.Resposta import Resposta
from models.Progresso import Progresso
from config.database import colecao_respostas, colecao_atividades, colecao_criancas, colecao_progresso
from schema.schemas import individual_serial, list_serial
from bson import ObjectId
from datetime import datetime, timezone

router = APIRouter()

# ROTA QUE RETORNA TODAS AS RESPOSTAS
@router.get("/todas_respostas")
async def listar_respostas():
    respostas = list_serial(colecao_respostas.find())
    return respostas

# ROTA QUE RETORNA RESPOSTA PELO ID
@router.get("/buscar_resposta/{id}")
async def buscar_resposta(
    id: str = Path(..., description="ID da resposta a ser buscada") 
):
    resposta = colecao_respostas.find_one({"_id": ObjectId(id)})
    if not resposta:
        raise HTTPException(status_code=404, detail="Resposta não encontrada")
    return individual_serial(resposta)

# ROTA QUE DELETA UMA RESPOSTA PELO ID
@router.delete("/deleta_resposta/{id}")
async def deleta_resposta(
    id: str = Path(..., description="ID da resposta a ser deletada") 
):
    resultado = colecao_respostas.find_one_and_delete({"_id": ObjectId(id)})
    if not resultado:
        raise HTTPException(status_code=404, detail="Resposta não encontrada para deletar")
    return {
        "mensagem": "Resposta deletada com sucesso"
    }

# função pra validar respostas na rota '/responder'
def validar_resposta(atividade: dict, resposta_texto: str):
    palavra = atividade.get("palavra", "").lower()
    tipo = atividade.get("tipo", "")
    if tipo == "quantidade_letras":
        if not resposta_texto.isdigit():
            raise HTTPException(status_code=400, detail="A resposta deve ser um número inteiro")
        correta = int(resposta_texto) == len(palavra)
        resposta_correta = len(palavra)
    elif tipo == "primeira_letra":
        correta = resposta_texto.lower() == palavra[0]
        resposta_correta = palavra[0]
    elif tipo == "ultima_letra":
        correta = resposta_texto.lower() == palavra[-1]
        resposta_correta = palavra[-1]
    else:
        raise HTTPException(status_code=400, detail="Tipo de atividade inválido ou não implementado")
    return correta, resposta_correta

# ROTA QUE RETORNA SE AS ATIVIDADES ESTAO CORRETAS
# Ainda precisa arrumar isso - Token ou sessao
# def get_crianca_id():
#     return "ID_DA_CRIANCA_LOGADA"

@router.post("/responder")
async def enviar_resposta(resposta: Resposta):
    # Pega o ID_CRIANCA do localStorage do Front-End
    crianca_id = resposta.crianca_id
    
    # Busca a atividade
    atividade = colecao_atividades.find_one({"_id": ObjectId(resposta.atividade_id)})
    if not atividade:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")

    # Valida a resposta
    correta, resposta_correta = validar_resposta(atividade, resposta.resposta)

    # Salva resposta no banco de respostas
    dados_resposta = resposta.model_dump()
    dados_resposta.update({
        "correta": correta,
        "resposta_correta": resposta_correta,
        "data": datetime.now(timezone.utc)
    })
    resultado = colecao_respostas.insert_one(dados_resposta)

    # Atualiza ou cria progresso
    progresso_existente = colecao_progresso.find_one({
        "crianca_id": crianca_id,
        "atividade_id": resposta.atividade_id
    })

    if progresso_existente:
        # Incrementa tentativas e atualiza resultado e nível
        colecao_progresso.update_one(
            {"_id": progresso_existente["_id"]},
            {
                "$inc": {"tentativas": 1},
                "$set": {
                    "resultado": "acerto" if correta else "erro",
                    "nivel": int(atividade.get("nivel", 1)),
                    "data": datetime.now(timezone.utc)
                }
            }
        )
    else:
        # Cria um novo progresso
        progresso_data = Progresso(
            crianca_id=crianca_id,
            atividade_id=resposta.atividade_id,
            resultado="acerto" if correta else "erro",
            tentativas=1,
            nivel=int(atividade.get("nivel", 1)),
            data=datetime.now(timezone.utc)
        )
        colecao_progresso.insert_one(progresso_data.model_dump())

    return {
        "id": str(resultado.inserted_id),
        "correta": correta,
        "resposta_correta": resposta_correta
    }