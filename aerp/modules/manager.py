from firebase_admin import auth
from flask import Blueprint, make_response, request, wrappers

from aerp.database.models.Manager import Manager

manager = Blueprint("manager", __name__, static_folder='/static')

@manager.route("/update-employee-data", methods=['POST'])  # type: ignore
def update_employee_data() -> wrappers.Response:
    payload = request.json
    accessToken = request.cookies.get("accessToken")
    try:
        authClaims = auth.verify_session_cookie(accessToken, check_revoked=True)
    except Exception:
        responseDict = {
            "status": "fail",
            "message": "ID token verification failed"
        }
        return make_response(responseDict, 401)

    manager = Manager(authClaims["uid"])
    manager.updateEmployeeData(userID=payload["user_id"], data=payload)
    response = {"status": "success"}
    return make_response(response, 200)

@manager.route("/get-jr-employees", methods=['GET'])  # type: ignore
def get_jr_employees() -> wrappers.Response:
    accessToken = request.cookies.get("accessToken")
    try:
        authClaims = auth.verify_session_cookie(accessToken, check_revoked=True)
    except Exception:
        response = {
            "status": "fail",
            "message": "ID token verification failed"
        }
        return make_response(response, 401)

    manager = Manager(authClaims["uid"])
    employees = manager.getAllJrEmployees()
    responseDict = {
        "status": "success",
        "employees": employees
    }
    return make_response(responseDict, 200)

@manager.route("/get-jr-managers", methods=['GET'])  # type: ignore
def get_jr_managers() -> wrappers.Response:
    accessToken = request.cookies.get("accessToken")
    try:
        authClaims = auth.verify_session_cookie(accessToken, check_revoked=True)
    except Exception:
        response = {
            "status": "fail",
            "message": "ID token verification failed"
        }
        return make_response(response, 401)

    manager = Manager(authClaims["uid"])
    managers = manager.getAllJrManagers()
    responseDict = {
        "status": "success",
        "employees": managers
    }
    return make_response(responseDict, 200)

@manager.route("/<str:user_id>/get-managers", methods=['GET'])  # type: ignore
def get_managers_of_employee(user_id: str) -> wrappers.Response:
    accessToken = request.cookies.get("accessToken")
    try:
        authClaims = auth.verify_session_cookie(accessToken, check_revoked=True)
    except Exception:
        response = {
            "status": "fail",
            "message": "ID token verification failed"
        }
        return make_response(response, 401)

    manager = Manager(authClaims["uid"])
    managers = manager.getAllManagersOfEmployee(userID=user_id)
    responseDict = {
        "status": "success",
        "employees": managers
    }
    return make_response(responseDict, 200)

@manager.route("/get-unassigned-employees", methods=['GET'])  # type: ignore
def get_unassigned_employees() -> wrappers.Response:
    accessToken = request.cookies.get("accessToken")
    try:
        authClaims = auth.verify_session_cookie(accessToken, check_revoked=True)
    except Exception:
        response = {
            "status": "fail",
            "message": "ID token verification failed"
        }
        return make_response(response, 401)

    manager = Manager(authClaims["uid"])
    employees = manager.getUnassignedEmployees()
    responseDict = {
        "status": "success",
        "employees": employees
    }
    return make_response(responseDict, 200)

@manager.route("/<str:user_id>/self-remove-manager", methods=['GET'])  # type: ignore
def self_remove_manager(user_id: str) -> wrappers.Response:
    accessToken = request.cookies.get("accessToken")
    try:
        authClaims = auth.verify_session_cookie(accessToken, check_revoked=True)
    except Exception:
        response = {
            "status": "fail",
            "message": "ID token verification failed"
        }
        return make_response(response, 401)

    manager = Manager(authClaims["uid"])
    manager.removeSelfAsManager(employee_uid=user_id)
    responseDict = {
        "status": "success"
    }
    return make_response(responseDict, 200)

@manager.route("/<str:employee_id>/remove-manager/<str:manager_id>", methods=['GET'])  # type: ignore
def remove_manager(employee_id: str, manager_id: str) -> wrappers.Response:
    accessToken = request.cookies.get("accessToken")
    try:
        authClaims = auth.verify_session_cookie(accessToken, check_revoked=True)
    except Exception:
        response = {
            "status": "fail",
            "message": "ID token verification failed"
        }
        return make_response(response, 401)

    manager = Manager(authClaims["uid"])
    managerRemoved = manager.removeManagerForEmployee(employee_uid=employee_id, manager_uid=manager_id)
    status = "success" if managerRemoved is True else "failure"
    responseDict = {
        "status": status
    }
    return make_response(responseDict, 200)

@manager.route("/<str:employee_id>/add-manager/<str:manager_id>", methods=['GET'])  # type: ignore
def add_manager(employee_id: str, manager_id: str) -> wrappers.Response:
    accessToken = request.cookies.get("accessToken")
    try:
        authClaims = auth.verify_session_cookie(accessToken, check_revoked=True)
    except Exception:
        response = {
            "status": "fail",
            "message": "ID token verification failed"
        }
        return make_response(response, 401)

    manager = Manager(authClaims["uid"])
    managerRemoved = manager.assignOtherManager(employee_uid=employee_id, manager_uid=manager_id)
    status = "success" if managerRemoved is True else "failure"
    responseDict = {
        "status": status
    }
    return make_response(responseDict, 200)

@manager.route("/mark-leave", methods=['POST'])  # type: ignore
def mark_leave() -> wrappers.Response:
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

    manager = Manager(authClaims["uid"])
    manager.markLeave(leaveID=payload["leave_id"], leaveStatus=payload["leave_status"])
    responseDict = {
        "status": "success"
    }
    return make_response(responseDict, 200)

@manager.route("/get-leave/<str:leaveType>", methods=['POST'])  # type: ignore
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

    manager = Manager(authClaims["uid"])
    leaves = []
    if leaveType == "pending":
        leaves = manager.getPendingLeaves()
    else:
        leaves = manager.getMarkedLeaves(leaveType=leaveType)
    responseDict = {
        "status": "success",
        "leaves": leaves
    }
    return make_response(responseDict, 200)
