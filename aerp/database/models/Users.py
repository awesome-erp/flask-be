from aerp.database.models.BaseModel import Base
from firebase_admin import auth
from aerp.database.dataValidity.user_data_validity import testAllInput, checkName,
                                                          checkDOB, checkEmail, checkPhone
from datetime import timedelta
from aerp.database.extractData.userDataExtraction import filterFieldsForUpdate
from typing import Optional, Any, Dict
import random
import string


class User(Base):
    """
    The User Model
    """
    def __init__(self, uid: str) -> None:
        """
        User Model initalization
        """
        self.init_database()
        self.uid = uid
        self.userDocument = self.database.document(self.uid)

    def setData(self, data: Dict[str, Any]) -> None:
        """
        Set User Data to the Data Base

        Parameters
        ----------
        Dict[str, Any]

        name: str
            Name of the User
        organization: str
            Name of the Organization
        dob: str
            Date of Birth of the User
        phone: str
            Phone number of the User
        personal_email: str
            Personal Email of the User
        email: str
            Organization Email of the User

        Returns
        -------
        None
        """
        userData = {
            "uid": self.uid,
            "name": data["name"],
            "organization": data["organization"],
            "dob": data["dob"],
            "phone": data["phone"],
            "email": data["email"],
            "personal_email": data["personal_email"],
            "role": "",
            "team_id": "",
            "is_manager": False,
            "employees": [],
            "salary": 0.0,
            "pending_leaves": {},
            "approved_leaves": {},
            "rejected_leaves": {},
            "self_approved_leaves": {},
            "self_rejected_leaves": {}
        }
        inputTestResult, failure = testAllInput(userData)
        if inputTestResult is True:
            self.userDocument.set(userData)
        else:
            raise Exception(f"Issues Detected in data: {failure}")

    def getData(self) -> Dict[str, Any]:
        """
        Get User data from database

        Returns
        -------
        Dict[str, Any]
            user_id: str
                id of the User
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
            salary: float
                Salary of User
        """
        data = self.userDocument.get().to_dict()
        userData = {
            "user_id": self.uid,
            "name": data["name"],
            "organization": data["organization"],
            "dob": data["dob"],
            "phone": data["phone"],
            "email": data["email"],
            "personal_email": data["personal_email"],
            "role": data["role"],
            "team_id": data["team_id"],
            "salary": data["salary"]
        }
        return userData

    def updateEditableData(self, data: Dict[str, Any]) -> None:
        """
        Update self editable fields for an user

        Prarameters 
        -----------
        Dict[str, Any]:
 
        name: Optional[str]
            If user wants to change name
        dob: Optional[str]
            If user wants to change dob
        phone: Optional[str]
            If user wants to change phone
        personal_email: Optional[str]
            If user wants to change personal_email

        Returns
        -------
        None
        """
        updateAbles = ["name", "dob", "phone", "personal_email"]
        data = filterFieldsForUpdate(fields=updateAbles, data=data)
        inputTestResult, failure = testAllInput(data)

        if inputTestResult is True:
            self.userDocument.update(userData)
        else:
            raise Exception(f"Issues Detected in data: {failure}")

    def createLeave(self, leaveStart: str, leaveEnd: str, leaveCreated: str, description: str):
        leaveID = self.uid + ''.join(random.choice(string.ascii_uppercase 
                                                   + string.ascii_lowercase 
                                                   + string.digits) for _ in range(10))
        userName = self.userDocument.get().to_dict()["name"]
        leave = {
                "leave_start": leaveStart,
                "leave_end": leaveEnd,
                "leave_created": leaveCreated,
                "marked_by_uid": "",
                "marked_by_name": "",
                "marked_by_email": "",
                "description": description
            }
        self.userDocument.update({
            f"pending_leaves.{leaveID}": leave
        })
