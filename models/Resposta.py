from pydantic import BaseModel 

class Resposta(BaseModel):
    atividade_id: str  # ID da atividade no Mongo
    resposta: str      # Resposta do usuário
