from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Annotated

class ResponsavelUpdate(BaseModel):
    nome: Optional[str] = Field(None, example="João da Silva")
    email: Optional[EmailStr] = Field(None, example="joao@email.com")
    telefone: Optional[Annotated[str, Field(pattern=r'^\d{11}$')]] = Field(None, example="11987654321")
    senha_atual: Optional[str] = Field(None, min_length=6)
    senha_nova: Optional[str] = Field(None, min_length=6)