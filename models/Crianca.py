from pydantic import BaseModel, Field, field_validator
from typing import Annotated
# from validate_docbr import CPF

class Crianca(BaseModel):
    cpf: Annotated[str, Field(min_length=11, max_length=11, pattern=r'^\d{11}$')]
    nome: str = Field(..., example="Roberto")
    data_nascimento: str = Field(..., example="2020-10-10")
    tipo_escola: str = Field(..., example="publica")
    responsavel_id: str

    # @field_validator("cpf")
    # def validar_cpf(cls, v):
    #     if not CPF().validate(v):
    #         raise ValueError("CPF inválido")
    #     return v