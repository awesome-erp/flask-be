from aerp.database.models.BaseModel import Base
from aerp.database.utils.userDataValidity import testAllInput
from aerp.database.utils.detailsExtraction import getAllDocs, extractFields, extractEmployeesFromStream

from firebase_admin import firestore
from typing import Any, Dict, List
import os

class Manager(Base):
    """
    The Manager Model
    """
    def __init__(self, uid: str) -> None:
        """
        User Model initalization
        """
        self.init_database()
        self.uid = uid
        self.document = self.database.document(self.uid)
        self.managerData = self.document.get().to_dict()
        if self.managerData["is_manager"] is not True and os.environ.get("ADMIN_EMAIL") != self.managerData["email"]:
            raise Exception("User Not a Manager")

    def getPendingRequests(self, reqType: str) -> List[Dict[str, Any]]:
        employees = self.managerData["employees"]
        reqs = self.requests_database.where("type", "==", reqType)\
                                     .where("creator_id", "in", employees)\
                                     .where("marked_as", "==", "pending")\
                                     .order_by("created", direction=firestore.Query.DESCENDING).stream()
        return getAllDocs(reqs)

    def getMarkedRequests(self, reqType: str, markedAs: str) -> List[Dict[str, Any]]:
        reqs = self.requests_database.where("type", "==", reqType)\
                                     .where("marked_by_uid", "==", self.uid)\
                                     .where("marked_as", "==", markedAs)\
                                     .order_by("created", direction=firestore.Query.DESCENDING).stream()
        return getAllDocs(reqs)

    def markRequest(self, reqID: str, marked: str) -> None:
        reqDoc = self.requests_database.document(reqID)
        req = {"marked_as": marked,
               "marked_by_uid": self.uid,
               "marked_by_name": self.managerData["name"],
               "marked_by_email": self.managerData["email"]}
        reqDoc.update(req)

    def updateEmployeeData(self, userID: str, data: Dict[str, Any]) -> None:
        """
        Update Managerial data for user
        """
        if userID in self.managerData["employees"]:
            userDetailsDoc = self.database.document(userID)
            fieldsToExtract = ["salary", "is_manager", "team_id", "role"]
            updateValue = extractFields(data=data, fields=fieldsToExtract)
            inputTestResult, failure = testAllInput(updateValue)
            if inputTestResult is True:
                userDetailsDoc.update(updateValue)
            else:
                raise Exception(f"Issues Detected in data: {failure}")

    def getAllJrEmployees(self) -> List[Dict[str, Any]]:
        """
        Get all employees under a particular manager
        """
        employees = self.managerData["employees"]
        employeesList = []
        increment = 10
        employeeCounter = 0
        while(employeeCounter < len(employees)):
            employeeData = self.database.where("user_id", "in", employees[employeeCounter:employeeCounter+increment])\
                                        .stream()
            fieldList = ["name", "dob", "phone", "email", "personal_email", "user_id", "manager_email",
                         "role", "team_id", "is_manager", "manager_id", "manager_name", "salary", "payments"]
            employeesList.extend(extractEmployeesFromStream(employees=employeeData, fields=fieldList))
            employeeCounter += increment
        return employeesList

    def getAllJrManagers(self) -> List[Dict[str, Any]]:
        """
        Get all managers under a particular manager
        """
        employees = self.managerData["employees"]
        employeesList = []
        increment = 10
        employeeCounter = 0
        while(employeeCounter < len(employees)):
            employeeData = self.database.where("user_id", "in", employees[employeeCounter:employeeCounter+increment])\
                                        .where("is_manager", "==", True)\
                                        .stream()
            fieldList = ["name", "dob", "phone", "email", "personal_email", "user_id", "manager_email",
                         "role", "team_id", "is_manager", "manager_id", "manager_name", "salary", "payments"]
            employeesList.extend(extractEmployeesFromStream(employees=employeeData, fields=fieldList))
            employeeCounter += increment
        return employeesList

    def getUnassignedEmployees(self) -> List[Dict[str, Any]]:
        """
        Get Employees that are not assigned to teams
        """
        employeeData = self.database.where("manager_id", "==", "").stream()
        fieldList = ["name", "dob", "phone", "email", "personal_email", "user_id", "manager_email",
                     "role", "team_id", "is_manager", "manager_id", "manager_name", "salary"]
        return extractEmployeesFromStream(employees=employeeData, fields=fieldList)

    def removeSelfAsManager(self, employee_uid: str) -> None:
        self.document.update({"employees": firestore.ArrayRemove([employee_uid])})
        self.database.document(employee_uid).update({"manager_id": "",
                                                     "manager_email": "",
                                                     "manager_name": ""})

    def assignOtherManager(self, manager_uid: str, employee_uid: str) -> bool:
        employees = set(self.managerData["employees"])
        managerData = self.database.document(manager_uid).get().to_dict()
        if (manager_uid in employees or manager_uid == self.uid):
            self.document.update({"employees": firestore.ArrayRemove([employee_uid])})
            self.database.document(manager_uid).update({"employees": firestore.ArrayUnion([employee_uid])})
            self.database.document(employee_uid).update({"manager_id": managerData["user_id"],
                                                         "manager_email": managerData["email"],
                                                         "manager_name": managerData["name"]})
            return True
        else:
            return False

    def removeManagerForEmployee(self, manager_uid: str, employee_uid: str) -> bool:
        employees = set(self.managerData["employees"])
        if manager_uid in employees and employee_uid in employees:
            self.database.document(manager_uid).update({"employees": firestore.ArrayRemove([employee_uid])})
            self.database.document(employee_uid).update({"manager_id": "",
                                                         "manager_email": "",
                                                         "manager_name": ""})
            return True
        else:
            return False

    def removeEmployee(self, userID: str) -> None:
        """
        Remove an employee and assign manager to all employees under the person
        to as self
        """
        employeeDoc = self.database.document(userID)
        employeeDict = employeeDoc.get().to_dict()
        employeeDoc.update({"salary": 0.0,
                            "is_manager": False,
                            "employees": [],
                            "team_id": "",
                            "manager_id": "",
                            "manager_email": "",
                            "manager_name": "",
                            "role": ""})
        self.document.update({"employees": firestore.ArrayRemove(userID)})
        for empID in employeeDict["employees"]:
            self.database.document(empID)\
                         .update({"manager_id": self.managerData["user_id"],
                                  "manager_email": self.managerData["email"],
                                  "manager_name": self.managerData["name"]})

    def markTransaction(self, userID: str, transaction: Dict[str, Any]) -> None:
        employeeDoc = self.database.document(userID)
        transactionDict = {
            "date": transaction["date"],
            "description": transaction["description"],
            "amount": transaction["amount"],
            "type": transaction["type"]
        }
        employeeDoc.update({"payments": firestore.ArrayUnion([transactionDict])})

    def filters(self, name: str = "", teamID: str = "", role: str = "", email: str = "") -> List[Dict[str, Any]]:
        query = self.database
        if email != "":
            query = query.where("email", "==", email)
        else:
            if name != "":
                query = query.where("name", "==", name)
            if role != "":
                query = query.where("role", "==", role)
            if teamID != "":
                query = query.where("team_id", "==", teamID)

        users = query.stream()
        fieldList = ["name", "dob", "phone", "email", "personal_email", "user_id", "manager_email",
                     "role", "team_id", "is_manager", "manager_id", "manager_name", "salary", "payments"]
        return extractEmployeesFromStream(employees=users, fields=fieldList)
