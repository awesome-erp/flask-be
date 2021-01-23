from aerp.database.models.BaseModel import Base
from aerp.database.utils.userDataValidity import testAllInput, compareDates
from aerp.database.utils.detailsExtraction import getAllDocs, extractFields

from firebase_admin import firestore
from typing import Any, Dict, List
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
        userData = {
            "user_id": self.uid,
            "name": data["name"],
            "dob": data["dob"],
            "phone": data["phone"],
            "email": data["email"],
            "personal_email": data["personalEmail"],
            "manager_id": "",
            "manager_email": "",
            "manager_name": "",
            "role": "",
            "team_id": "",
            "team_name": "",
            "is_manager": False,
            "is_team_lead": False,
            "is_admin": False,
            "employees": [],
            "salary": 0.0,
            "payments": []
        }
        inputTestResult, failure = testAllInput(userData)
        if inputTestResult is True:
            self.userDocument.set(userData)
        else:
            raise Exception(f"Issues Detected in data: {failure}")

    def getData(self) -> Dict[str, Any]:
        data = self.userDocument.get().to_dict()
        userData = {
            "user_id": data["user_id"],
            "name": data["name"],
            "dob": data["dob"],
            "phone": data["phone"],
            "email": data["email"],
            "personal_email": data["personal_email"],
            "role": data["role"],
            "team_id": data["team_id"],
            "team_name": data["team_name"],
            "salary": data["salary"],
            "is_manager": data["is_manager"],
            "manager_id": data["salary"],
            "manager_name": data["manager_name"],
            "manager_email": data["manager_email"],
            "payments": data["payments"]
        }
        return userData

    def updateEditableData(self, data: Dict[str, Any]) -> None:
        updateAbles = ["name", "dob", "phone", "personal_email"]
        data = extractFields(fields=updateAbles, data=data, returnEmpty=False)
        inputTestResult, failure = testAllInput(data)

        if inputTestResult is True:
            self.userDocument.update(data)
        else:
            raise Exception(f"Issues Detected in data: {failure}")

    def createLeaveRequest(self, leaveInput: Dict[str, str]) -> None:
        leaveID = self.uid + "-" + ''.join(random.choice(string.ascii_uppercase
                                                         + string.ascii_lowercase
                                                         + string.digits) for _ in range(10))
        user = self.userDocument.get().to_dict()
        leaveDoc = self.requests_database.document(leaveID)
        createDateComp = compareDates(leaveInput["leaveCreated"], leaveInput["leaveStart"])
        startendDateComp = compareDates(leaveInput["leaveStart"], leaveInput["leaveEnd"])
        if createDateComp != (True, "<"):
            raise Exception("Leave Must start after Current date")
        if startendDateComp != (True, ">") or startendDateComp != (True, "="):
            raise Exception("Leave Must start before end date")
        leave = {"leave_id": leaveID,
                 "type": "leave",
                 "creator_name": user["name"],
                 "creator_id": self.uid,
                 "creator_email": user["email"],
                 "leave_start": leaveInput["leaveStart"],
                 "leave_end": leaveInput["leaveEnd"],
                 "created": leaveInput["leaveCreated"],
                 "marked_as": "pending",
                 "marked_by_uid": "",
                 "marked_by_name": "",
                 "marked_by_email": "",
                 "description": leaveInput["description"]}
        leaveDoc.set(leave)

    def createLoanRaiseRequest(self, details: Dict[str, str]) -> None:
        loanRaiseID = self.uid + "-" + ''.join(random.choice
                                               (string.ascii_uppercase
                                                + string.ascii_lowercase
                                                + string.digits) for _ in range(10))
        user = self.userDocument.get().to_dict()
        loanRaiseDoc = self.requests_database.document(loanRaiseID)
        loanRaise = {"id": loanRaiseID,
                     "type": details["type"].lower(),
                     "creator_name": user["name"],
                     "creator_id": self.uid,
                     "creator_email": user["email"],
                     "amount": details["amount"],
                     "created": details["created"],
                     "marked_as": "pending",
                     "marked_by_uid": "",
                     "marked_by_name": "",
                     "marked_by_email": "",
                     "description": details["description"]}
        loanRaiseDoc.set(loanRaise)

    def getRequests(self, reqType: str, markedAs: str) -> List[Dict[str, Any]]:
        reqs = self.requests_database.where("type", "==", reqType)\
                                     .where("creator_id", "==", self.uid)\
                                     .where("marked_as", "==", markedAs)\
                                     .order_by("created", direction = firestore.Query.DESCENDING)\
                                     .stream()

        return getAllDocs(reqs)
