from pydantic import BaseModel, EmailStr, Field
from typing import Annotated, List, Optional
# from validate_docbr import CPF

class Responsavel(BaseModel):
    cpf: Annotated[str, Field(min_length=11, max_length=11, pattern=r'^\d{11}$')]
    nome: str
    email: EmailStr
    telefone: Annotated[str, Field(pattern=r'^\d{11}$')]
    senha: Annotated[str, Field(min_length=6)]
    filhos: Optional[List[str]] = Field(default_factory=list)

    # @field_validator("cpf")
    # def validar_cpf(cls, v):
    #     if not CPF().validate(v):
    #         raise ValueError("CPF inválido")
    #     return v
