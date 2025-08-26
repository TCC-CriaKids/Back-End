from pydantic import BaseModel, Field
from typing import Annotated

class Crianca(BaseModel):
    cpf: Annotated[str, Field(min_length=11, max_length=11, pattern=r'^\d{11}$')]  # CPF 11 dígitos
    nome: str = Field(..., example="Roberto")
    data_nascimento: str = Field(..., example="2020-10-10")  
    tipo_escola: str = Field(..., example="publica")