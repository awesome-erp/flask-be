from typing import Dict, Any, Tuple
from datetime import datetime
import re


def checkName(name: str) -> bool:
    """
    Checks if a string is a valid name
    Only spaces and alphabets allowed

    Parameters
    ----------
    name: str
        The name to be Tested

    Returns
    -------
    bool
        True/False according to the validity of the name
    """

    return type(name) == str and bool(re.match(r'[a-zA-Z\s]+$', name))


def checkDate(date: str) -> bool:
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
    if not type(date) == str:
        return False
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except Exception:
        return False
    return True

def compareDates(date1: str, date2: str) -> Tuple[bool, str]:
    """
    Checks if a string is a valid dob

    Parameters
    ----------
    dob: str
        The name to be Tested

    Returns
    -------
    Tuple(bool, str)
        True/False according to the validity of the dates
        "<"|">"|"="|"Error" is the sign between 1st and 2nd date
    """
    if checkDate(date1) and checkDate(date2):
        dateObj1 = datetime.strptime(date1, "%Y-%m-%d")
        dateObj2 = datetime.strptime(date2, "%Y-%m-%d")
        if dateObj1 > dateObj2:
            return (True, ">")
        elif dateObj1 < dateObj2:
            return (True, "<")
        else:
            return (True, "=")
    else:
        return (False, "Error")


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

    return type(email) == str and bool(re.match(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', email))


def checkPhone(phone: str) -> bool:
    """
    Checks if a phone number is valid
    Expected Countrycode<space>Number +91 12345678901

    Parameters
    ----------
    phone: str
        The string to be Tested

    Returns
    -------
    bool
        True/False according to the validity of the phone number
    """

    return type(phone) == str and phone.split()[-1].isnumeric()


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
        if not checkDate(Inputs["dob"]):
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
