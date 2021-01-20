from datetime import timedelta
from firebase_admin import auth
from flask import Blueprint, request, wrappers

from aerp.database.models.User import User
from aerp.utils.authorization import checkPermission
from aerp.utils.responses import success, failure

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
        return failure(code=401)

    expiry = timedelta(days=7)
    timeLimitedAuthToken = auth.create_session_cookie(idToken, expires_in=expiry)
    userDetails = {
        "access_token": timeLimitedAuthToken,
        "email": authClaims["email"]
    }
    response = success("user_details", userDetails, 200)
    response.set_cookie('accessToken', timeLimitedAuthToken, secure=True,
                        domain="awesome-erp.github.io", httponly=True, samesite="Strict")

    return response


@authorization.route("/set-user-data", methods=['POST'])  # type: ignore
def set_user_data() -> wrappers.Response:
    """
    Route to set user data for 1st time
    """
    payload = request.json
    try:
        authClaims = checkPermission(request)
    except Exception:
        return failure(code=401)

    user = User(authClaims["uid"])
    payload["email"] = authClaims["email"]
    user.setData(payload)
    return success("user_id", user.uid, 200)


@authorization.route("/sign-out", methods=['GET'])  # type: ignore
def remCookie() -> wrappers.Response:
    """
    Remove the HTTP only coocie for login
    """
    response = success(code=200)
    response.set_cookie('accessToken', '', expires=0, secure=True,
                        domain="awesome-erp.github.io", httponly=True, samesite="None")
    return response
