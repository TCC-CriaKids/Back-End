from pydantic import BaseModel
from datetime import datetime

class Crianca(BaseModel):
    cpf: str
    nome: str
    data_nascimento: datetime
