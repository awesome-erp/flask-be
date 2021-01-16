from firebase_admin import auth
from flask import Blueprint, make_response, request, wrappers

from aerp.database.models.User import User

employee = Blueprint("employee", __name__, static_folder='/static')

@employee.route("/info", methods=['POST'])  # type: ignore
def info() -> wrappers.Response:
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

@employee.route("/update-data", methods=['POST'])  # type: ignore
def update_data() -> wrappers.Response:
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

@employee.route("/create-leave", methods=['POST'])  # type: ignore
def create_leave() -> wrappers.Response:
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
    user.createLeave(payload)
    responseDict = {
        "status": "success",
    }
    return make_response(responseDict, 200)

@employee.route("/leave/<str:leaveType>", methods=['GET'])  # type: ignore
def get_leave(leaveType: str) -> wrappers.Response:
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
    leaves = user.getLeaves(leaveType=leaveType)
    responseDict = {
        "status": "success",
        "leaves": leaves
    }
    return make_response(responseDict, 200)
