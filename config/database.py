from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Carrega as variáveis do .env
load_dotenv()

# Pega a URL do MongoDB do .env
MONGO_URI = os.getenv("MONGO_URI")

# Conecta ao MongoDB
client = MongoClient(MONGO_URI)

db = client.cria_kids

colecao_respostas = db['resposta']
colecao_atividades = db["atividade"]
colecao_responsaveis = db['responsavel']
colecao_criancas = db['crianca']
colecao_promptollama = db['promptollama']
colecao_progresso = db['progresso']