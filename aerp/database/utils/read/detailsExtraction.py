from typing import Any, Dict, List, Generator

def getAllDocs(docs: Generator) -> List[Dict[str, Any]]:
    docsList = []
    for doc in docs:
        docDict = doc.to_dict()
        docsList.append(docDict)

    return docsList
