from fastapi import APIRouter
import requests
from config.database import colecao_promptollama  # nova coleção para armazenar
from datetime import datetime

router = APIRouter()

OLLAMA_URL = "http://localhost:11434/api/generate"

@router.post("/ask-ollama/")
async def ask_ollama(prompt: str):
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }
    
    response = requests.post(OLLAMA_URL, json=payload)
    result = response.json()

    # Salvar no MongoDB (colecao_conversas)
    colecao_promptollama.insert_one({
        "prompt": prompt,
        "resposta_modelo": result.get("response", ""),
        "created_at": datetime.now()
    })

    # Retorna só a resposta do modelo
    return {"resposta": result.get("response", "")}