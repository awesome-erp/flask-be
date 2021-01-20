from flask import Blueprint, request, wrappers

from aerp.database.models.User import User
from aerp.utils.authorization import checkPermission
from aerp.utils.responses import success, failure

employee = Blueprint("employee", __name__, static_folder='/static')

@employee.route("/info", methods=['GET'])  # type: ignore
def info() -> wrappers.Response:
    try:
        authClaims = checkPermission(request)
    except Exception:
        return failure(code=401)
    user = User(authClaims["uid"])
    userData = user.getData()
    return success("user_data", userData, 200)

@employee.route("/update-data", methods=['POST'])  # type: ignore
def update_data() -> wrappers.Response:
    payload = request.json
    try:
        authClaims = checkPermission(request)
    except Exception:
        return failure(code=401)
    user = User(authClaims["uid"])
    user.updateEditableData(payload)
    return success(code=200)

@employee.route("/create-leave", methods=['POST'])  # type: ignore
def create_leave() -> wrappers.Response:
    payload = request.json
    try:
        authClaims = checkPermission(request)
    except Exception:
        return failure(code=401)
    user = User(authClaims["uid"])
    user.createLeaveRequest(payload)
    return success(code=200)

@employee.route("/create-loan-raise-request", methods=['POST'])  # type: ignore
def create_loan_raise_request() -> wrappers.Response:
    payload = request.json
    try:
        authClaims = checkPermission(request)
    except Exception:
        return failure(code=401)
    user = User(authClaims["uid"])
    user.createLoanRaiseRequest(payload)
    return success(code=200)

@employee.route("/<string:reqType>/<string:markedAs>", methods=['GET'])  # type: ignore
def get_leave(reqType: str, markedAs: str) -> wrappers.Response:
    try:
        authClaims = checkPermission(request)
    except Exception:
        return failure(code=401)
    user = User(authClaims["uid"])
    req = user.getRequests(reqType=reqType, markedAs=markedAs)
    return success(reqType, req, 200)
