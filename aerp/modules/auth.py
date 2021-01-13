from datetime import timedelta
from firebase_admin import auth
from flask import Blueprint, make_response, request
from aerp.database.models.Auth import Auth
from aerp.modules.utils.auth_utils import dataSanitization, getTimeLimitedToken


authorization = Blueprint("auth", __name__, static_folder='/static')


@authorization.route("/sign-user", methods=['POST'])  # type: ignore
def sign_user() -> object:
    """
    Route for user SIGN in token verification
    """
    payload = request.json
    idToken = payload["idToken"]
    try:
        user = auth.verify_id_token(idToken)
    except Exception:
        responseDict = {
            "status": "fail",
            "message": "ID token verification failed"
        }
        return make_response(responseDict, 401)

    expiry = timedelta(days=7)
    timeLimitedAuthToken = auth.create_session_cookie(self.authToken, expires_in=expiry)
    responseDict = {
        "status": "success",
        "accessToken": timeLimitedAuthToken
    }
    response = make_response(responseDict, 200)
    response.set_cookie('accessToken', timeLimitedAuthToken, secure=True,
                        httponly=True, samesite="Strict")

    return response


@authorization.route("/set-user-data", methods=['POST'])  # type: ignore
def set_user_data() -> object:
    """
    Route to set user data for 1st time
    """
    payload = request.json
    accessToken = request.cookies.get("accessToken")
    try:
        user = auth.verify_session_cookie(accessToken, check_revoked=True)
    except Exception:
        response = {
            "status": "fail",
            "message": "ID token verification failed"
        }
        return make_response(response, 401)

    userPersonalData = dataSanitization(postData)
    user.setData(**userPersonalData)
    responseDict = {
        "status": "success",
        "user_id": user.uid
    }
    return make_response(responseDict, 200)


@authorization.route("/sign-out", methods=['GET'])  # type: ignore
def remCookie() -> object:
    """
    Remove the HTTP only coocie for login
    """
    response = make_response({"status": "success"}, 200)
    response.set_cookie('accessToken', '', expires=0, secure=True, httponly=True, samesite="None")
    return response
