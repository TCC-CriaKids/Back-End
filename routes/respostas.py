from fastapi import APIRouter, HTTPException, Depends
from models.Resposta import Resposta
from config.database import colecao_respostas, colecao_atividades, colecao_criancas
from schema.schemas import individual_serial, list_serial
from bson import ObjectId

router = APIRouter()

# ROTA QUE RETORNA TODAS AS RESPOSTAS
@router.get("/todas-respostas")
async def listar_respostas():
    respostas = list_serial(colecao_respostas.find())
    return respostas

# ROTA QUE RETORNA RESPOSTA PELO ID
@router.get("/buscar-resposta")
async def buscar_resposta(id: str):
    resposta = colecao_respostas.find_one({"_id": ObjectId(id)})
    if not resposta:
        raise HTTPException(status_code=404, detail="Resposta não encontrada")
    return individual_serial(resposta)

# ROTA QUE DELETA UMA RESPOSTA PELO ID
@router.delete("/deleta-resposta")
async def deleta_resposta(id: str):
    resultado = colecao_respostas.find_one_and_delete({"_id": ObjectId(id)})
    if not resultado:
        raise HTTPException(status_code=404, detail="Resposta não encontrada para deletar")
    return {
        "mensagem": "Resposta deletada com sucesso"
    }

# ROTA QUE RETORNA SE AS ATIVIDADES ESTAO CORRETAS
# Ainda precisa arrumar isso - Token ou sessao
def get_crianca_id():
    return "ID_DA_CRIANCA_LOGADA"

@router.post("/responder")
async def enviar_resposta(resposta: Resposta, crianca_id: str = Depends(get_crianca_id)):
    # Busca a atividade
    atividade = colecao_atividades.find_one({"_id": ObjectId(resposta.atividade_id)})
    if not atividade:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")

    palavra = atividade.get("palavra", "").lower()
    tipo = atividade.get("tipo", "")
    
    # Verifica se a resposta está correta
    if tipo == "quantidade_letras":
        if not resposta.resposta.isdigit():
            raise HTTPException(status_code=400, detail="A resposta deve ser um número inteiro")
        correta = int(resposta.resposta) == len(palavra)
        resposta_correta = len(palavra)
    elif tipo == "primeira_letra":
        correta = resposta.resposta.lower() == palavra[0]
        resposta_correta = palavra[0]
    elif tipo == "ultima_letra":
        correta = resposta.resposta.lower() == palavra[-1]
        resposta_correta = palavra[-1]
    else:
        raise HTTPException(status_code=400, detail="Tipo de atividade inválido ou não implementado")

    # Salva resposta no banco de respostas
    dados_resposta = resposta.model_dump()
    dados_resposta.update({
        "correta": correta,
        "resposta_correta": resposta_correta,
        "crianca_id": crianca_id
    })
    resultado = colecao_respostas.insert_one(dados_resposta)

    # Atualiza o progresso da criança
    crianca = colecao_criancas.find_one({"_id": ObjectId(crianca_id)})
    if not crianca:
        raise HTTPException(status_code=404, detail="Criança não encontrada")

    progresso = crianca.get("progresso", [])
    existente = next((a for a in progresso if a["atividade_id"] == resposta.atividade_id), None)
    if existente:
        existente["acertos"] = existente.get("acertos", 0) + int(correta)
        existente["nivel"] = atividade.get("nivel", 1)
    else:
        progresso.append({
            "atividade_id": resposta.atividade_id,
            "acertos": int(correta),
            "nivel": atividade.get("nivel", 1)
        })
    colecao_criancas.update_one({"_id": ObjectId(crianca_id)}, {"$set": {"progresso": progresso}})

    return {
        "id": str(resultado.inserted_id),
        "correta": correta,
        "resposta_correta": resposta_correta
    }