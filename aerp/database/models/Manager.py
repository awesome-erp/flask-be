from aerp.database.models.BaseModel import Base
from aerp.database.utils.write.user_data_validity import testAllInput
from aerp.database.utils.read.leaveExtraction import getAllLeaves
from aerp.database.utils.read.userDataExtraction import extractFields, extractEmployeesFromUID, extractEmployeesFromStream

from firebase_admin import firestore
from typing import Any, Dict, List

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
        if self.managerData["is_manager"] is not True:
            raise Exception("User Not a Manager")

    def getPendingLeaves(self) -> List[Dict[str, Any]]:
        """
        Get All Pending Leaves of the employees

        Returns
        -------
        List[Dict[str, Any]]
            uid: User id
            user_name: Name of employee
            leave_id: str
            leave_start: "dd-mm-yyyy"
            leave_end: "dd-mm-yyyy"
            leave_created: "dd-mm-yyyy"
            description: any notes related to the leaves

        """
        employees = self.managerData["employees"]
        leaves = self.leaves_database.where("creator_id", "in", employees)\
                                     .where("marked_as", "==", "pending")\
                                     .order_by("leave_created", direction=firestore.Query.DESCENDING).stream()
        return getAllLeaves(leaves=leaves)

    def getMarkedLeaves(self, leaveType: str) -> List[Dict[str, Any]]:
        """
        Get All Pending Leaves of the employees

        Returns
        -------
        List[Dict[str, Any]]
            uid: User id
            user_name: Name of employee
            leave_id: str
            leave_start: "dd-mm-yyyy"
            leave_end: "dd-mm-yyyy"
            leave_created: "dd-mm-yyyy"
            description: any notes related to the leaves
        """
        leaves = self.leaves_database.where("marked_by_uid", "==", self.uid)\
                                     .where("marked_as", "==", leaveType)\
                                     .order_by("leave_created", direction=firestore.Query.DESCENDING).stream()
        return getAllLeaves(leaves=leaves)

    def markLeave(self, leaveID: str, leaveStatus: str) -> None:
        """
        This function deletes a pending leave and adds to the approved leaves
        This updates the manager document as well and adds it
        """
        leaveDoc = self.leave_database.document(leaveID)
        leave = {"marked_as": leaveStatus,
                 "marked_by_uid": self.uid,
                 "marked_by_name": self.managerData["name"],
                 "marked_by_email": self.managerData["email"]}
        leaveDoc.update(leave)

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
        return extractEmployeesFromUID(self.database, employees=employees)

    def getAllJrManagers(self) -> List[Dict[str, Any]]:
        """
        Get all managers under a particular manager
        """
        employees = self.managerData["employees"]
        employeeData = self.database.where("uid", "in", employees)\
                                    .where("is_manager", "==", True)\
                                    .stream()
        fieldList = ["name", "dob", "phone", "email", "personal_email", "uid",
                     "role", "team_id", "is_manager", "manager_id", "salary"]
        return extractEmployeesFromStream(employees=employeeData, fields=fieldList)

    def getAllManagersOfEmployee(self, userID: str) -> List[Dict[str, Any]]:
        """
        Get all managers of a particular employee
        """
        employees = set(self.managerData["employees"])
        managersData = self.database.where("employees", "array_contains", userID)\
                                    .stream()
        fieldList = ["name", "dob", "phone", "email", "personal_email", "user_id",
                     "role", "team_id", "is_manager", "manager_id", "salary"]
        managers = extractEmployeesFromStream(employees=managersData, fields=fieldList)
        for manager in managers:
            if manager["user_id"] in employees:
                manager["removeable"] = True
            else:
                manager["removeable"] = False
        return managers

    def getUnassignedEmployees(self) -> List[Dict[str, Any]]:
        """
        Get Employees that are not assigned to teams
        """
        employeeData = self.database.where("team_id", "==", "").stream()
        fieldList = ["name", "dob", "phone", "email", "personal_email", "user_id",
                     "role", "team_id", "is_manager", "manager_id", "salary"]
        return extractEmployeesFromStream(employees=employeeData, fields=fieldList)

    def removeSelfAsManager(self, employee_uid: str) -> None:
        self.document.update({"employees": firestore.ArrayRemove([employee_uid])})

    def assignOtherManager(self, manager_uid: str, employee_uid: str) -> bool:
        employees = set(self.managerData["employees"])
        if manager_uid in employees and employee_uid in employees:
            self.database.document(manager_uid).update({"employees": firestore.ArrayUnion([employee_uid])})
            return True
        else:
            return False

    def removeManagerForEmployee(self, manager_uid: str, employee_uid: str) -> bool:
        employees = set(self.managerData["employees"])
        if manager_uid in employees and employee_uid in employees:
            self.database.document(manager_uid).update({"employees": firestore.ArrayRemove([employee_uid])})
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
                            "team_id": "",
                            "role": "",
                            "pending_leaves": {},
                            "approved_leaves": {},
                            "rejected_leaves": {},
                            "self_rejected_leaves": {},
                            "self_approved_leaves": {}})
        self.document.update({"employees": firestore.ArrayUnion(employeeDict["employees"])})
