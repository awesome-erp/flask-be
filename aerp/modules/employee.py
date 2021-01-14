from firebase_admin import auth
from flask import Blueprint, make_response, request
from aerp.database.models.Users import User

employee = Blueprint("auth", __name__, static_folder='/static')


@employee.route("/info", methods=['POST'])  # type: ignore
def info() -> object:
    accessToken = request.cookies.get("accessToken")
    try:
        authClaims = auth.verify_session_cookie(accessToken, check_revoked=True)
    except Exception:
        responseDict = {
            "status": "fail",
            "message": "ID token verification failed"
        }
        return make_response(responseDict, 401)

    user = User(authClaims["uid"])
    userData = user.getData()
 
    return make_response(userData, 401)

@authorization.route("/update-data", methods=['POST'])  # type: ignore
def set_user_data() -> object:
    payload = request.json
    accessToken = request.cookies.get("accessToken")
    try:
        authClaims = auth.verify_session_cookie(accessToken, check_revoked=True)
    except Exception:
        response = {
            "status": "fail",
            "message": "ID token verification failed"
        }
        return make_response(response, 401)
    user = User(authClaims["uid"])
    user.updateEditableData(payload)
    responseDict = {
        "status": "success",
    }
    return make_response(responseDict, 200)

@authorization.route("/create-leave", methods=['GET'])  # type: ignore
def create_leave() -> object:
    payload = request.json
    accessToken = request.cookies.get("accessToken")
    try:
        authClaims = auth.verify_session_cookie(accessToken, check_revoked=True)
    except Exception:
        response = {
            "status": "fail",
            "message": "ID token verification failed"
        }
        return make_response(response, 401)
    user = User(authClaims["uid"])
    user.createLeave (payload)
    responseDict = {
        "status": "success",
    }
    return make_response(responseDict, 200)
