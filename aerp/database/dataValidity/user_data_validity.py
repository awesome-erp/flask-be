from typing import Dict, Any, Tuple
from datetime import datetime


def checkName(name: str) -> bool:
    """
    Checks if a string is a valid name

    Parameters
    ----------
    name: str
        The name to be Tested

    Returns
    -------
    bool
        True/False according to the validity of the name
    """

    return type(name) == str and name.isalpha()


def checkDOB(dob: str) -> bool:
    """
    Checks if a string is a valid dob

    Parameters
    ----------
    dob: str
        The name to be Tested

    Returns
    -------
    bool
        True/False according to the validity of the dob
    """
    if not type(dob) == str:
        return False
    try:
        datetime.strptime(dob, "%d-%m-%Y")
    except Exception:
        return False

    return True


def checkEmail(email: str) -> bool:
    """
    Checks if a string is a valid email

    Parameters
    ----------
    email: str
        The email to be Tested

    Returns
    -------
    bool
        True/False according to the validity of the email
    """

    return type(email) == str


def checkPhone(phone: str) -> bool:
    """
    Checks if a phone number is valid

    Parameters
    ----------
    phone: str
        The string to be Tested

    Returns
    -------
    bool
        True/False according to the validity of the phone number
    """

    return type(phone) == str


def testAllInput(Inputs: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Tests All Inputs for their validity

    Parameters
    ----------
    Inputs: Dict[str, Any]
        The Set of Key value Pair holding field names and their values

    Returns
    -------
    bool
        False if any Input is invalid, True if all tests pass
    str
        The field for which the test failed
    """

    if "name" in Inputs:
        if not checkName(Inputs["name"]):
            return (False, "name")
    if "organization" in Inputs:
        if not checkName(Inputs["name"]):
            return (False, "name")
    if "dob" in Inputs:
        if not checkDOB(Inputs["dob"]):
            return (False, "dob")
    if "phone" in Inputs:
        if not checkPhone(Inputs["phone"]):
            return (False, "phone")
    if "email" in Inputs:
        if not checkEmail(Inputs["email"]):
            return (False, "email")
    if "personalEmail" in Inputs:
        if not checkEmail(Inputs["personalEmail"]):
            return (False, "personalEmail")

    return (True, "None")
