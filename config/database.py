from pymongo import MongoClient
# Importa a classe MongoClient da biblioteca pymongo, que permite conectar ao banco de dados MongoDB.

client = MongoClient("mongodb+srv://raphaluvi:MMaX9NhzNOj2Ka1j@cluster0.dvam31v.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
# Cria uma conexão com o MongoDB Atlas (banco de dados na nuvem), usando a URL de conexão.
# Essa URL contém o usuário, a senha e as configurações de cluster.

db = client.cria_kids
# Acessa (ou cria, caso não exista) o banco de dados chamado "cria_kids".

colecao_respostas = db['resposta']
colecao_atividades = db["atividade"]
colecao_responsaveis = db['responsavel']
colecao_criancas = db['crianca']
colecao_promptollama = db['promptollama']
colecao_progresso = db['progresso']