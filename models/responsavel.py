from pydantic import BaseModel, EmailStr, Field
from typing import Annotated

class Responsavel(BaseModel):
    cpf: Annotated[str, Field(min_length=11, max_length=11, pattern=r'^\d{11}$')]
    nome: str
    email: EmailStr
    telefone: Annotated[str, Field(pattern=r'^\d{10,15}$')]
    senha: str
