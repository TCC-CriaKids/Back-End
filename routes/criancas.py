from fastapi import APIRouter, HTTPException, Path
from models.Crianca import Crianca
from models.CriancaUpdate import CriancaUpdate
from config.database import colecao_responsaveis, colecao_criancas
from schema.schemas import individual_serial, list_serial
from bson import ObjectId
import bcrypt

router = APIRouter()

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

@router.post("/cadastra-crianca")
async def cadastrar_crianca(crianca: Crianca):
    # Verifica se já existe CPF cadastrado
    if colecao_criancas.find_one({"cpf": crianca.cpf}):
        raise HTTPException(status_code=400, detail="CPF já cadastrado.")
    
    # Verifica se o responsável existe
    responsavel = colecao_responsaveis.find_one({"_id": ObjectId(crianca.responsavel_id)})
    if not responsavel:
        raise HTTPException(status_code=404, detail="Responsável não encontrado.")
    
    # Criptografa a senha
    senha_hash = bcrypt.hashpw(crianca.senha.encode('utf-8'), bcrypt.gensalt())
    
    # Cria dicionário dos dados para inserir, substituindo a senha pela hash
    dados_crianca = crianca.model_dump()
    dados_crianca["senha"] = senha_hash.decode('utf-8')

    # Insere no banco
    resultado = colecao_criancas.insert_one(dados_crianca)
    nova_crianca = colecao_criancas.find_one({"_id": resultado.inserted_id})

    # Serializando os dados sem a senha
    dados_serializados = individual_serial(nova_crianca)
    dados_serializados.pop("senha", None)

    return {
        "mensagem": "Criança cadastrada com sucesso!",
        "dados": dados_serializados
    }

@router.put("/crianca/{id}")
async def atualizar_crianca(
    id: str = Path(..., description="ID da criança a ser atualizada"),
    dados: CriancaUpdate = ...
):
    crianca = colecao_criancas.find_one({"_id": ObjectId(id)})
    if not crianca:
        raise HTTPException(status_code=404, detail="Criança não encontrada.")

    dados_dict = dados.model_dump(exclude_unset=True)

    # Troca de senha
    if 'senha_atual' in dados_dict or 'senha_nova' in dados_dict:
        if not dados_dict.get('senha_atual') or not dados_dict.get('senha_nova'):
            raise HTTPException(status_code=400, detail="Informe senha atual e nova senha para alteração.")
        
        if not bcrypt.checkpw(dados_dict['senha_atual'].encode('utf-8'), crianca['senha'].encode('utf-8')):
            raise HTTPException(status_code=400, detail="Senha atual incorreta.")

        nova_senha_hash = bcrypt.hashpw(dados_dict['senha_nova'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        dados_dict['senha'] = nova_senha_hash

        dados_dict.pop('senha_atual')
        dados_dict.pop('senha_nova')

    # Protege campos que não devem ser alterados
    dados_dict.pop('cpf', None)
    dados_dict.pop('responsavel_id', None)
    dados_dict.pop('progresso', None)

    if not dados_dict:
        raise HTTPException(status_code=400, detail="Nenhum dado para atualizar.")

    colecao_criancas.update_one({"_id": ObjectId(id)}, {"$set": dados_dict})

    crianca_atualizada = colecao_criancas.find_one({"_id": ObjectId(id)})
    dados_serializados = individual_serial(crianca_atualizada)
    dados_serializados.pop("senha", None)

    return {
        "mensagem": "Dados da criança atualizados com sucesso!",
        "dados": dados_serializados
    }