from typing import Any, Dict, List

def extractFields(data: Dict[str, Any], fields: List[str], returnEmpty: bool = True) -> Dict[str, Any]:
    """
    Extracts the Listed Params from the dict
    """
    cleanedData = {}
    for field in fields:
        if field in data:
            if returnEmpty is False and data[field] in ["", None, {}, []]:
                continue
            cleanedData[field] = data[field]

    return cleanedData

def extractEmployeesFromStream(employees: Any, fields: List[str]) -> List[Dict[str, Any]]:
    """
    Extract employees from a Stream
    """
    employeesList = []
    for employee in employees:
        employeeDict = employee.to_dict()
        employeesList.append(extractFields(employeeDict, fields=fields))

    return employeesList

def getAllDocs(docs: Any) -> List[Dict[str, Any]]:
    docsList = []
    for doc in docs:
        docDict = doc.to_dict()
        docsList.append(docDict)

    return docsList
