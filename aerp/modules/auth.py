from datetime import timedelta
from firebase_admin import auth
from flask import Blueprint, make_response, request, wrappers

from aerp.database.models.User import User
from .utils import checkPermission


authorization = Blueprint("auth", __name__, static_folder='/static')


@authorization.route("/sign-user", methods=['POST'])  # type: ignore
def sign_user() -> wrappers.Response:
    """
    User SIGN in token verification and cookie creation
    """
    payload = request.json
    idToken = payload["idToken"]
    try:
        authClaims = auth.verify_id_token(idToken)
    except Exception:
        responseDict = {
            "status": "fail",
            "message": "ID token verification failed"
        }
        print(type(make_response(responseDict, 401)))
        return make_response(responseDict, 401)

    expiry = timedelta(days=7)
    timeLimitedAuthToken = auth.create_session_cookie(idToken, expires_in=expiry)
    responseDict = {
        "status": "success",
        "accessToken": timeLimitedAuthToken,
        "email": authClaims["email"]
    }
    response = make_response(responseDict, 200)
    response.set_cookie('accessToken', timeLimitedAuthToken, secure=True,
                        domain="awesome-erp.github.io", httponly=True, samesite="Strict")

    return response


@authorization.route("/set-user-data", methods=['POST'])  # type: ignore
def set_user_data() -> wrappers.Response:
    """
    Route to set user data for 1st time
    """
    payload = request.json
    accessToken = request.cookies.get("accessToken")
    try:
        authClaims = checkPermission(request)
    except Exception:
        response = {
            "status": "fail",
            "message": "ID token verification failed"
        }
        return make_response(response, 401)

    user = User(authClaims["uid"])
    payload["email"] = authClaims["email"]
    user.setData(payload)
    responseDict = {
        "status": "success",
        "user_id": user.uid
    }
    return make_response(responseDict, 200)


@authorization.route("/sign-out", methods=['GET'])  # type: ignore
def remCookie() -> wrappers.Response:
    """
    Remove the HTTP only coocie for login
    """
    response = make_response({"status": "success"}, 200)
    response.set_cookie('accessToken', '', expires=0, secure=True,
                        domain="awesome-erp.github.io", httponly=True, samesite="None")
    return response
