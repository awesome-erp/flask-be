from aerp.database.models.BaseModel import Base
from firebase_admin import auth
from aerp.database.dataValidity.Users import testAllInput, checkName, \
                                             checkDOB, checkEmail, checkPhone
from datetime import timedelta
from typing import Optional


class User(Base):

    def __init__(self, authToken: str):
        self.database = self.init_database().collection("user_profiles")
        self.authToken = authToken
        self.userClaims = self.getUserClaims()
        self.uid = self.userClaims["uid"]
        self.userDocument = self.database.document(self.uid)

    def getTimeLimitedToken(self, expiry: timedelta):
        return auth.create_session_cookie(self.authToken, expires_in=expiry)

    def getUserClaims(self):
        try:
            userClaims = auth.verify_session_cookie(self.authToken,
                                                    check_revoked=True)
            return userClaims
        except Exception:
            raise BaseException("Invalid access Token")

    def setData(self, dob: str, phone: str, personal_email: str,
                role: str, team_id: str, organization: str,
                name: Optional[str] = None):
        """
        Set User Data to the Data Base

        Parameters
        ----------
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
        role: str
            Role of User
        team_id: str
            Team id of User

        Returns
        -------
        bool
            True/False according to the status: set or not
        """
        if not name:
            name = self.userClaims["name"]
        userData = {
            "name": name,
            "organization": organization,
            "dob": dob,
            "phone": phone,
            "email": self.userClaims["email"],
            "personal_email": personal_email,
            "role": role,
            "team_id": team_id,
            "salary": 0.0
        }
        testAllInput(userData)
        self.userDocument.set(userData)

    def getData(self):
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
            "email": self.userClaims["email"],
            "personal_email": data["personal_email"],
            "role": data["role"],
            "team_id": data["team_id"],
            "salary": data["salary"]
        }
        return userData

    def updateUserEditableData(self, name: Optional[str] = None,
                               dob: Optional[str] = None,
                               phone: Optional[str] = None,
                               personal_email: Optional[str] = None):
        """
        Update self editable fields

        Prarameters
        -----------
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
        bool:
            True/False according to the status of the operation
        """
        userData = {}
        if name and checkName(name):
            userData["name"] = name
        if dob and checkDOB(dob):
            userData["dob"] = dob
        if phone and checkPhone(phone):
            userData["phone"] = phone
        if personal_email and checkEmail(personal_email):
            userData["personal_email"] = personal_email

        self.userDocument.update(userData)
