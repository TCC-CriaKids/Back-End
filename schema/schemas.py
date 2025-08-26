def individual_serial(document: dict) -> dict:
    serialized = document.copy()
    serialized["id"] = str(serialized.pop("_id"))
    return serialized

def list_serial(documents) -> list:
    return [individual_serial(doc) for doc in documents]
