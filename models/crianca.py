from pydantic import BaseModel, Field
from typing import Annotated
from datetime import date

class Crianca(BaseModel):
    cpf: Annotated[str, Field(min_length=11, max_length=11, pattern=r'^\d{11}$')]  # CPF 11 dígitos
    nome: str  
    data_nascimento: date  