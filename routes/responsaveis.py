from fastapi import APIRouter, HTTPException, Path
from models.Responsavel import Responsavel
from models.ResponsavelUpdate import ResponsavelUpdate
from config.database import colecao_responsaveis
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

    # Serializa, nao exibindo a senha antes de retornar
    dados_serializados = individual_serial(novo_responsavel)
    dados_serializados.pop("senha", None)  # Remove senha da resposta

    return {
        "mensagem": "Responsável cadastrado com sucesso!",
        "dados": dados_serializados
    }

@router.put("/responsavel/{id}")
async def atualizar_responsavel(
    id: str = Path(..., description="ID do responsável a ser atualizado"),
    dados: ResponsavelUpdate = ...
):
    responsavel = colecao_responsaveis.find_one({"_id": ObjectId(id)})
    if not responsavel:
        raise HTTPException(status_code=404, detail="Responsável não encontrado.")

    dados_dict = dados.model_dump(exclude_unset=True)

    # Troca de senha
    if 'senha_atual' in dados_dict or 'senha_nova' in dados_dict:
        if not dados_dict.get('senha_atual') or not dados_dict.get('senha_nova'):
            raise HTTPException(status_code=400, detail="Para trocar a senha, informe a senha atual e a nova senha.")

        if not bcrypt.checkpw(dados_dict['senha_atual'].encode('utf-8'), responsavel['senha'].encode('utf-8')):
            raise HTTPException(status_code=400, detail="Senha atual incorreta.")

        nova_senha_hash = bcrypt.hashpw(dados_dict['senha_nova'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        dados_dict['senha'] = nova_senha_hash

        dados_dict.pop('senha_atual')
        dados_dict.pop('senha_nova')

    # Protege campos que não devem ser alterados
    dados_dict.pop('cpf', None)

    if not dados_dict:
        raise HTTPException(status_code=400, detail="Nenhum dado para atualizar.")

    colecao_responsaveis.update_one({"_id": ObjectId(id)}, {"$set": dados_dict})

    responsavel_atualizado = colecao_responsaveis.find_one({"_id": ObjectId(id)})
    dados_serializados = individual_serial(responsavel_atualizado)
    dados_serializados.pop('senha', None)

    return {
        "mensagem": "Dados do responsável atualizados com sucesso!",
        "dados": dados_serializados
    }