from aerp.database.models.BaseModel import Base
from firebase_admin import auth
from aerp.database.dataValidity.user_data_validity import testAllInput, checkName, checkDOB, checkEmail, checkPhone
from datetime import timedelta
from typing import Optional, Any, Dict
import random
import string


class Auth(Base):
    """
    The User Model
    """
    def __init__(self, authToken: str) -> None:
        """
        User Model initalization
        """
        self.authToken = authToken
        self.userClaims = self.getUserClaims()
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

    def init_user(self, dob: str, phone: str, personal_email: str,
                email: str, role: str, team_id: str, organization: str,
                name: str) -> None:
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
        email: str
            Organization Email of the User
        role: str
            Role of User
        team_id: str
            Team id of User

        Returns
        -------
        None
        """
        userData = {
            "uid": self.uid,
            "name": name,
            "organization": organization,
            "dob": dob,
            "phone": phone,
            "email": email,
            "personal_email": personal_email,
            "role": role,
            "team_id": team_id,
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
