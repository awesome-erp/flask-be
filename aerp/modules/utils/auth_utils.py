from typing import Dict, Any


def clearDataForSet(dataInput: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sanitizes input data to output proper fields

    Parameters
    ----------
    dataInput: Dict[str, Any]
        A dictionary which consists of multiple fields

    Returns
    -------
    Dict[str, Any]
        name: str
            Name of the User
        organization: str
            Name of the Organisation
        dob: str
            Date of Birth of the User
        phone: str
            Phone number of the User
        email: str
            Organisation Email of the User
        personal_email: str
            Personal Email of the User
        role: str
            Role of User
        team_id: str
            Team id of User
    """
    dataOutput = {}
    if "name" in dataInput:
        dataOutput["name"] = dataInput["name"]
    if "organization" in dataInput:
        dataOutput["organization"] = dataInput["organization"]
    if "dob" in dataInput:
        dataOutput["dob"] = dataInput["dob"]
    if "phone" in dataInput:
        dataOutput["phone"] = dataInput["phone"]
    if "email" in dataInput:
        dataOutput["email"] = dataInput["email"]
    if "personal_email" in dataInput:
        dataOutput["personal_email"] = dataInput["personal_email"]
    if "role" in dataInput:
        dataOutput["role"] = dataInput["role"]
    if "team_id" in dataInput:
        dataOutput["team_id"] = dataInput["team_id"]

    return dataOutput
