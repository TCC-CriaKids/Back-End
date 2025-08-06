from pydantic import BaseModel

class Responsavel(BaseModel):
    cpf: str
    nome: str
    email: str
    telefone: int
    senha: str