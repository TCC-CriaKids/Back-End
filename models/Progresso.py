from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional

class Progresso(BaseModel):
    crianca_id: str = Field(..., description="ID da criança")
    atividade_id: str = Field(..., description="ID da atividade")
    resultado: str = Field(..., description="Resultado da última tentativa: 'acerto' ou 'erro'")
    tentativas: int = Field(1, description="Número de tentativas realizadas")
    nivel: Optional[int] = Field(1, description="Nível da atividade")
    data: Optional[datetime] = Field(default_factory=datetime.now(timezone.utc), description="Data/hora do registro do progresso")
