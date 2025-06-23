from fastapi import APIRouter, HTTPException
from models.resposta import Resposta
from config.database import colecao_respostas, colecao_atividades
from schema.schemas import individual_serial, list_serial
from bson import ObjectId

router = APIRouter()

# ROTA QUE RETORNA TODAS AS RESPOSTAS
@router.get("/")
async def listar_respostas():
    respostas = list_serial(colecao_respostas.find())
    return respostas

# ROTA QUE RETORNA RESPOSTA PELO ID
@router.get("/{id}")
async def buscar_resposta(id: str):
    resposta = colecao_respostas.find_one({"_id": ObjectId(id)})
    if not resposta:
        raise HTTPException(status_code=404, detail="Resposta não encontrada")
    return individual_serial(resposta)

# ROTA QUE DELETA UMA RESPOSTA PELO ID
@router.delete("/{id}")
async def deleta_resposta(id: str):
    resultado = colecao_respostas.find_one_and_delete({"_id": ObjectId(id)})
    if not resultado:
        raise HTTPException(status_code=404, detail="Resposta não encontrada para deletar")
    return {
        "mensagem": "Resposta deletada com sucesso"
    }

# ROTA QUE RETORNA SE AS ATIVIDADES ESTAO CORRETAS
@router.post("/")
async def enviar_resposta(resposta: Resposta):
    atividade = colecao_atividades.find_one({"_id": ObjectId(resposta.atividade_id)})
    if not atividade:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")

    correta = False
    
    palavra = atividade.get("palavra", "").lower()
    
    tipo = atividade.get("tipo", "")

    # Verifica o tipo da atividade: primeira_letra, ultima_letra, quantidade_letras
    if tipo == "quantidade_letras":
        if resposta.resposta.isdigit():
            resposta_correta = len(palavra)
            correta = int(resposta.resposta) == len(palavra)
        else:
            raise HTTPException(status_code=400, detail="A resposta deve ser um número inteiro")
    elif tipo == "primeira_letra":
        resposta_correta = palavra[0]
        correta = resposta.resposta.lower() == palavra[0]
    elif tipo == "ultima_letra":
        resposta_correta = palavra[-1]
        correta = resposta.resposta.lower() == palavra[-1]
    else:
        raise HTTPException(status_code=400, detail="Tipo de atividade inválido ou não implementado")

    dados_resposta = resposta.model_dump()
    
    dados_resposta["correta"] = correta
    dados_resposta["resposta_correta"] = resposta_correta
    
    resultado = colecao_respostas.insert_one(dados_resposta)
    return {
        "id": str(resultado.inserted_id), 
        "correta": correta
    }