from fastapi import APIRouter, HTTPException
from models.Atividade import Atividade
from config.database import colecao_atividades
from schema.schemas import individual_serial, list_serial
from bson import ObjectId
import random

router = APIRouter()

# ROTA QUE RETORNA TODAS AS ATIVIDADES
@router.get("/todas-atividades")
async def listar_atividades():
    atividades = list_serial(colecao_atividades.find())
    return atividades

# ROTA QUE RETORNA ATIVIDADE PELO ID
@router.get("/buscar-atividade")
async def buscar_atividade(id: str):
    atividade = colecao_atividades.find_one({"_id": ObjectId(id)})
    if not atividade:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    return individual_serial(atividade)

# ROTA QUE DELETA UMA ATIVIDADE PELO ID
@router.delete("/deleta-atividade")
async def deleta_atividade(id: str):
    resultado = colecao_atividades.find_one_and_delete({"_id": ObjectId(id)})
    if not resultado:
        raise HTTPException(status_code=404, detail="Atividade não encontrada para deletar")
    return {
        "mensagem": "Atividade deletada com sucesso"
    }

# Lista fixa de palavras para sortear
palavras = [
    "casa", "bola", "gato", "livro", "carro", "flor", "sol", "lua", "pão", "árvore",
    "água", "fogo", "vento", "mesa", "cadeira", "janela", "porta", "cachorro", "peixe", "rio",
    "mar", "montanha", "praia", "céu", "estrela", "nuvem", "festa", "amor", "paz", "luz",
    "cor", "verde", "azul", "vermelho", "amarelo", "preto", "branco", "rosa", "laranja", "cinza",
    "mão", "pé", "olho", "boca", "nariz", "orelha", "cabeça", "coração", "alma", "vida",
    "dia", "noite", "tempo", "vento", "chuva", "neve", "fruta", "maçã", "banana", "laranja",
    "uva", "melancia", "morango", "abacaxi", "tomate", "cenoura", "batata", "alface", "arroz", "feijão",
    "leite", "queijo", "pão", "bolo", "doces", "ferramenta", "martelo", "serrote", "prego", "tesoura",
    "computador", "celular", "telefone", "televisão", "rádio", "livro", "caderno", "caneta", "lápis", "borracha",
    "escola", "professor", "aluno", "amigo", "familia", "trabalho", "cidade", "campo", "carro", "ônibus"
]
tipos_validos = {
    "primeira_letra", 
    "ultima_letra", 
    "quantidade_letras"
}

# ROTA QUE CRIA A ATIVIDADE (ESCOLHE A PALAVRA ALEATORIAMENTE)
@router.post("/cria-atividade")
async def criar_atividade(atividade: Atividade):
    if atividade.tipo not in tipos_validos:
        raise HTTPException(status_code=400, detail="Tipo de atividade inválido")
    
    palavra_escolhida = random.choice(palavras)
    
    dados_atividade = atividade.model_dump()
    dados_atividade["palavra"] = palavra_escolhida
    
    resultado = colecao_atividades.insert_one(dados_atividade)
    return {
        "id": str(resultado.inserted_id), 
        "palavra": palavra_escolhida
    }

