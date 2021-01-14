from aerp.database.models.BaseModel import Base
from aerp.database.utils.write.user_data_validity import testAllInput
from aerp.database.utils.read.userDataExtraction import extractFields

from typing import Any, Dict
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
        data = extractFields(fields=updateAbles, data=data, returnEmpty=False)
        inputTestResult, failure = testAllInput(data)

        if inputTestResult is True:
            self.userDocument.update(data)
        else:
            raise Exception(f"Issues Detected in data: {failure}")

    def createLeave(self, leaveInput: Dict[str, str]) -> None:
        leaveID = self.uid + ''.join(random.choice(string.ascii_uppercase
                                                   + string.ascii_lowercase
                                                   + string.digits) for _ in range(10))
        user = self.userDocument.get().to_dict()
        leave = {"creator_name": user["name"],
                 "creator_id": self.uid,
                 "creator_email": user["email"],
                 "leave_start": leaveInput["leaveStart"],
                 "leave_end": leaveInput["leaveEnd"],
                 "leave_created": leaveInput["leaveCreated"],
                 "marked_by_uid": "",
                 "marked_by_name": "",
                 "marked_by_email": "",
                 "description": leaveInput["description"]}
        self.userDocument.update({f"pending_leaves.{leaveID}": leave})
