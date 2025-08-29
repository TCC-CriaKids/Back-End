from pydantic import BaseModel, Field
from typing import Annotated, List, Optional
from models.Atividade import Atividade  # model ja existente

class Crianca(BaseModel):
    cpf: Annotated[str, Field(min_length=11, max_length=11, pattern=r'^\d{11}$')]
    nome: str = Field(..., example="Roberto")
    data_nascimento: str = Field(..., example="2020-10-10")
    tipo_escola: str = Field(..., example="publica")
    senha: Annotated[str, Field(min_length=6)]  # senha para login da criança
    responsavel_id: str
    progresso: Optional[List[Atividade]] = Field(default_factory=list)  # lista de atividades feitas