# def individual_serial(todo) -> dict:
#     # Converte um documento MongoDB para um dicionário JSON serializável
#     return {
#         "id": str(todo["_id"]),  # Converte o ObjectId para string
#         "name": todo["name"],  # Campo name
#         "description": todo["description"],  # Campo description
#         "complete": todo["complete"]  # Campo complete
#     }

# def list_serial(todos) -> list:
#     # Converte uma lista de documentos MongoDB em uma lista de dicionários JSON
#     return [individual_serial(todo) for todo in todos]

def individual_serial(document) -> dict:
    return {
        "id": str(document["_id"]),
        **{k: v for k, v in document.items() if k != "_id"}
    }

def list_serial(documents) -> list:
    return [individual_serial(doc) for doc in documents]
