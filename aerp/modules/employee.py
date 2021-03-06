from flask import Blueprint, request, wrappers

from aerp.database.models.User import User
from aerp.utils.authorization import checkPermission
from aerp.utils.responses import success, failure

employee = Blueprint("employee", __name__, static_folder='/static')

@employee.route("/info", methods=['GET'])  # type: ignore
def info() -> wrappers.Response:
    """
    Get User Info
    """
    try:
        authClaims = checkPermission(request)
    except Exception:
        return failure(code=401)
    user = User(authClaims["uid"])
    userData = user.getData()
    return success("user_data", userData, 200)

@employee.route("/update-data", methods=['POST'])  # type: ignore
def update_data() -> wrappers.Response:
    """
    Update the data that is only accessable to user
    """
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
    """
    Allows User to request for leaves

    Input Expected(All Compulsory)
    ------------------------------
    {
        "leave_start": "yyyy-mm-dd",
        "leave_end": "yyyy-mm-dd",
        "created": "yyyy-mm-dd",
        "description": "Some Random reason"
    }
    """
    payload = request.json
    try:
        authClaims = checkPermission(request)
    except Exception:
        return failure(code=401)
    user = User(authClaims["uid"])
    try:
        user.createLeaveRequest(payload)
    except Exception as e:
        return failure("error", str(e), code=400)
    return success(code=200)

@employee.route("/create-loan-raise-request", methods=['POST'])  # type: ignore
def create_loan_raise_request() -> wrappers.Response:
    """
    Allows User to request for loan or raise

    Input Expected(All Compulsory)
    ------------------------------
    {
        "type": "loan/raise",
        "amount": 100.10,
        "created": "yyyy-mm-dd",
        "description": "Some Random reason"
    }
    """
    payload = request.json
    try:
        authClaims = checkPermission(request)
    except Exception:
        return failure(code=401)
    user = User(authClaims["uid"])
    user.createLoanRaiseRequest(payload)
    return success(code=200)

@employee.route("/<string:reqType>/<string:markedAs>", methods=['GET'])  # type: ignore
def get_request(reqType: str, markedAs: str) -> wrappers.Response:
    """
    Get the details of the request

    URL_PARAMS
    ----------
    reqType: str
        can be one of "leave"|"loan"|"raise"
    markedAs: str
        can be one of "pending"|"accept"|"reject"

    """
    try:
        authClaims = checkPermission(request)
    except Exception:
        return failure(code=401)
    user = User(authClaims["uid"])
    req = user.getRequests(reqType=reqType, markedAs=markedAs)
    return success(reqType, req, 200)
