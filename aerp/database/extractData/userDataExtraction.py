from typing import Optional, Any, Dict, List

def extractFields(data: Dict[str, Any], fields: List[str]) -> Dict[str, Any]:
    """
    Extracts the Listed Params from the dict

    Parameters
    ----------
    data: Dict[str, Any]
        The data to extract fields from
    fields: List[str] 
        The list of fields whose data is to be extracted
    
    Return
    ------
    Dict[str, Any]
        Extracted Data
    """
    cleanedData = {}
    for field in fields:
        if field in data:
            cleanedData[field] = data[field]
    
    return cleanedData

def extractEmployeesFromUID(database, employees: List) -> Dict[str, Any]:
    """
    Extracts the Employees from the given list and a database

    Parameters
    ----------
    employees: Dict[str, Any]
    
    Return
    ------
    Dict[str, Any]
        List of employees
    """
    employeesList = []
    fieldList = ["name", "dob", "phone", "email", "personal_email", "uid",
                 "role", "team_id", "is_manager", "manager_id", "salary"]
    for employee in employees:
        employeeDict = database.document(employee).get().to_dict()
        employeesList.append(extractFields( employeeDict, fields=fieldList))

    return employeesList


def extractEmployeesFromStream(employees: Any, fields: List[str]) -> Dict[str, Any]:
    """
    Extract employees from a Stream
    """
    employeesList = []
    for employee in employees:
        employeeDict = employee.to_dict()
        employeesList.append(extractFields(employeeDict, fields=fields))

    return employeesList