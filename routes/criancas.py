from fastapi import APIRouter, HTTPException, Path
from models.Crianca import Crianca
from models.CriancaUpdate import CriancaUpdate
from config.database import colecao_responsaveis, colecao_criancas
from schema.schemas import individual_serial, list_serial
from bson import ObjectId
from validate_docbr import CPF

router = APIRouter()

# ROTA QUE RETORNA TODAS AS CRIANÇAS
@router.get("/todas_criancas")
async def listar_criancas():
    criancas = list_serial(colecao_criancas.find())
    if not criancas:
        raise HTTPException(status_code=404, detail="Não há registros de crianças")
    return criancas

# ROTA QUE RETORNA CRIANÇA PELO ID
@router.get("/buscar_crianca/{id}")
async def buscar_crianca(
    id: str = Path(..., description="ID da criança a ser buscada") 
):
    crianca = colecao_criancas.find_one({"_id": ObjectId(id)})
    if not crianca:
        raise HTTPException(status_code=404, detail="Criança não encontrada")
    return individual_serial(crianca)

# ROTA QUE DELETA CRIANÇA PELO ID 
@router.delete("/deleta_crianca/{id}")
async def deletar_crianca(
    id: str = Path(..., description="ID da criança a ser deletada")
):
    # Deleta a criança da coleção de crianças
    crianca = colecao_criancas.find_one_and_delete({"_id": ObjectId(id)})
    if not crianca:
        raise HTTPException(status_code=404, detail="Criança não encontrada para deletar")

    # Remove a referência da criança na lista de filhos do responsável
    colecao_responsaveis.update_many(
        {"filhos": ObjectId(id)},
        {"$pull": {"filhos": ObjectId(id)}}
    )

    return {
        "mensagem": "Criança deletada com sucesso"
    }

# ROTA DE CADASTRO DE CRIANÇA
cpf_validator = CPF()

@router.post("/cadastra_crianca")
async def cadastrar_crianca(crianca: Crianca):
    # Verifica se já existe CPF cadastrado
    if colecao_criancas.find_one({"cpf": crianca.cpf}):
        raise HTTPException(status_code=400, detail="CPF já cadastrado.")
    
    # Valida CPF real - DEIXA COMENTADO PARA TESTES
    # if not CPF().validate(crianca.cpf):
    #     raise HTTPException(status_code=400, detail="CPF inválido.")

    responsavel = colecao_responsaveis.find_one({"_id": ObjectId(crianca.responsavel_id)})
    if not responsavel:
        raise HTTPException(status_code=404, detail="Responsável não encontrado.")

    dados_crianca = crianca.model_dump()
    resultado = colecao_criancas.insert_one(dados_crianca)

    # atualizando a lista de filhos do responsavel
    colecao_responsaveis.update_one(
        {"_id": ObjectId(crianca.responsavel_id)},
        {"$push": {"filhos": str(resultado.inserted_id)}}
    ) 

    dados_serializados = individual_serial({**dados_crianca, "_id": resultado.inserted_id})

    return {
        "mensagem": "Criança cadastrada com sucesso!",
        "dados": dados_serializados
    }


@router.put("/atualiza_crianca/{id}")
async def atualizar_crianca(
    id: str = Path(..., description="ID da criança a ser atualizada"),
    dados: CriancaUpdate = ...
):
    crianca = colecao_criancas.find_one({"_id": ObjectId(id)})
    if not crianca:
        raise HTTPException(status_code=404, detail="Criança não encontrada.")

    dados_dict = dados.model_dump(exclude_unset=True)

    # Protege campos que não devem ser alterados
    dados_dict.pop('cpf', None)
    dados_dict.pop('responsavel_id', None)
    dados_dict.pop('progresso', None)

    if not dados_dict:
        raise HTTPException(status_code=400, detail="Nenhum dado para atualizar.")

    colecao_criancas.update_one({"_id": ObjectId(id)}, {"$set": dados_dict})

    crianca_atualizada = colecao_criancas.find_one({"_id": ObjectId(id)})
    dados_serializados = individual_serial(crianca_atualizada)

    return {
        "mensagem": "Dados da criança atualizados com sucesso!",
        "dados": dados_serializados
    }