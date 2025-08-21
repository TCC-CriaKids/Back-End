from fastapi import APIRouter, HTTPException
from models.responsavel import Responsavel
from models.crianca import Crianca
from config.database import colecao_responsaveis, colecao_criancas
from schema.schemas import individual_serial, list_serial
from bson import ObjectId
import bcrypt

router = APIRouter()


### RESPONSÁVEL

# ROTA QUE RETORNA TODOS OS RESPONSAVEIS
@router.get("/todos-responsaveis")
async def listar_responsaveis():
    responsaveis = list_serial(colecao_responsaveis.find())
    if not responsaveis:
        raise HTTPException(status_code=404, detail="Não há registros de responsáveis")
    return responsaveis

# ROTA QUE RETORNA RESPONSAVEL PELO ID
@router.get("/buscar-responsavel")
async def buscar_responsavel(id: str):
    responsavel = colecao_responsaveis.find_one({"_id": ObjectId(id)})
    if not responsavel:
        raise HTTPException(status_code=404, detail="Responsável não encontrado")
    return individual_serial(responsavel)

# ROTA QUE DELETA RESPONSÁVEL PELO ID
@router.delete("/deleta-responsavel")
async def deletar_responsavel(id: str):
    resultado = colecao_responsaveis.find_one_and_delete({"_id": ObjectId(id)})
    if not resultado:
        raise HTTPException(status_code=404, detail="Responsável não encontrado para deletar")
    return {
        "mensagem": "Responsável deletado com sucesso"
    }

@router.post("/cadastra-responsavel")
async def cadastrar_responsavel(responsavel: Responsavel):
    # Verifica se já existe CPF cadastrado
    if colecao_responsaveis.find_one({"cpf": responsavel.cpf}):
        raise HTTPException(status_code=400, detail="CPF já cadastrado.")

    # Criptografa a senha
    senha_hash = bcrypt.hashpw(responsavel.senha.encode('utf-8'), bcrypt.gensalt())
    
    # Cria dicionário dos dados para inserir, substituindo a senha pela hash
    dados_responsavel = responsavel.model_dump()
    dados_responsavel["senha"] = senha_hash.decode('utf-8')

    # Insere no banco
    resultado = colecao_responsaveis.insert_one(dados_responsavel)
    novo_responsavel = colecao_responsaveis.find_one({"_id": resultado.inserted_id})

    # Serializa, omitindo a senha antes de retornar
    dados_serializados = individual_serial(novo_responsavel)
    dados_serializados.pop("senha", None)  # Remove senha da resposta

    return {
        "mensagem": "Responsável cadastrado com sucesso!",
        "dados": dados_serializados
    }
    

### CRIANÇA

# ROTA QUE RETORNA TODAS AS CRIANÇAS
@router.get("/todas-criancas")
async def listar_criancas():
    criancas = list_serial(colecao_criancas.find())
    if not criancas:
        raise HTTPException(status_code=404, detail="Não há registros de crianças")
    return criancas

# ROTA QUE RETORNA CRIANÇA PELO ID
@router.get("/buscar-crianca")
async def buscar_crianca(id: str):
    crianca = colecao_criancas.find_one({"_id": ObjectId(id)})
    if not crianca:
        raise HTTPException(status_code=404, detail="Criança não encontrada")
    return individual_serial(crianca)

# ROTA QUE DELETA CRIANÇA PELO ID
@router.delete("/deleta-crianca")
async def deletar_crianca(id: str):
    crianca = colecao_criancas.find_one_and_delete({"_id": ObjectId(id)})
    if not crianca: 
        raise HTTPException(status_code=404, detail="Criança não encontrada para deletar")
    return {
        "mensagem": "Criança deletada com sucesso"
    }