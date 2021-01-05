from aerp.database.models.BaseModel import Base
from firebase_admin import auth
from aerp.database.dataValidity.user_data_validity import testAllInput, checkName, checkDOB, checkEmail, checkPhone
from datetime import timedelta
from typing import Optional, Any, Dict


class User(Base):
    """
    The User Model
    """
    def __init__(self, authToken: str) -> None:
        """
        User Model initalization
        """
        self.database = self.init_database().collection("user_profiles")
        self.authToken = authToken
        self.userClaims = self.getUserClaims()
        self.uid = self.userClaims["uid"]
        self.userDocument = self.database.document(self.uid)

    def getTimeLimitedToken(self, expiry: timedelta) -> str:
        """
        This returns a token with Limited validity

        Parameters
        ----------
        expiry: datetime.timedelta
            The datetime.timedelta object with the required validity

        Returns
        -------
        str
            The token with limited validity
        """
        return auth.create_session_cookie(self.authToken, expires_in=expiry)

    def getUserClaims(self) -> Dict[str, Any]:
        """
        This function fetches the custom claims of the users

        Returns
        -------
        dict
            The details of users stored in the custom claims
        """
        try:
            userClaims = auth.verify_session_cookie(self.authToken, check_revoked=True)
            return userClaims
        except Exception:
            raise BaseException("Invalid access Token")

    def setData(self, dob: str, phone: str, personal_email: str,
                role: str, team_id: str, organization: str,
                name: Optional[str] = None) -> None:
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
        None
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
        inputTestResult, failure = testAllInput(userData)[0]
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
                               personal_email: Optional[str] = None) -> None:
        """
        Update self editable fields for an user

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
        None
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
