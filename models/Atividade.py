from pydantic import BaseModel
# Importa a classe BaseModel da biblioteca Pydantic, que é usada para validação de dados e criação de modelos de dados no FastAPI.

class Atividade(BaseModel):
    tipo: str
    nivel: str = 1
    palavra: str = None # preenchido aleatoriamente na rota
    historia: str # princesas, heroi, fada, monstro
