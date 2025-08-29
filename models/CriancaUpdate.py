from pydantic import BaseModel, Field
from typing import Annotated, List, Optional
from models.Atividade import Atividade  # model ja existente

class CriancaUpdate(BaseModel):
    nome: Optional[str] = Field(..., example="Roberto")
    tipo_escola: Optional[str] = Field(..., example="publica")
    senha_atual: Optional[str] = Field(None, min_length=6)
    senha_nova: Optional[str] = Field(None, min_length=6)