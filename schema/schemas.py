def individual_serial(document) -> dict:
    return {
        "id": str(document["_id"]),
        **{k: v for k, v in document.items() if k != "_id"}
    }

def list_serial(documents) -> list:
    return [individual_serial(doc) for doc in documents]
