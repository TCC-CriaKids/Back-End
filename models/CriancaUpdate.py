from pydantic import BaseModel, Field
from typing import Optional

class CriancaUpdate(BaseModel):
    nome: Optional[str] = Field(..., example="Roberto")
    tipo_escola: Optional[str] = Field(..., example="publica")