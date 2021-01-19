from firebase_admin import auth
from flask import Blueprint, make_response, request, wrappers

from aerp.database.models.Manager import Manager
from aerp.utils.auth import checkPermission
from aerp.utils.responses import success, failure

manager = Blueprint("manager", __name__, static_folder='/static')

@manager.route("/update-employee-data", methods=['POST'])  # type: ignore
def update_employee_data() -> wrappers.Response:
    payload = request.json
    try:
        authClaims = checkPermission(request)
        manager = Manager(authClaims["uid"])
    except Exception:
        return failure(code=401)
    manager.updateEmployeeData(userID=payload["user_id"], data=payload)
    return success(code=200)

@manager.route("/get-jr-employees", methods=['GET'])  # type: ignore
def get_jr_employees() -> wrappers.Response:
    try:
        authClaims = checkPermission(request)
        manager = Manager(authClaims["uid"])
    except Exception:
        return failure(code=401)
    employees = manager.getAllJrEmployees()
    return success("employees", employees, 200)

@manager.route("/get-jr-managers", methods=['GET'])  # type: ignore
def get_jr_managers() -> wrappers.Response:
    try:
        authClaims = checkPermission(request)
        manager = Manager(authClaims["uid"])
    except Exception:
        return failure(code=401)
    managers = manager.getAllJrManagers()
    return success("managers", managers, 200)

@manager.route("/get-unassigned-employees", methods=['GET'])  # type: ignore
def get_unassigned_employees() -> wrappers.Response:
    try:
        authClaims = checkPermission(request)
        manager = Manager(authClaims["uid"])
    except Exception:
        return failure(code=401)
    employees = manager.getUnassignedEmployees()
    return success("employees", employees, 200)

@manager.route("/<string:user_id>/self-remove-manager", methods=['GET'])  # type: ignore
def self_remove_manager(user_id: str) -> wrappers.Response:
    try:
        authClaims = checkPermission(request)
        manager = Manager(authClaims["uid"])
    except Exception:
        return failure(code=401)
    manager.removeSelfAsManager(employee_uid=user_id)
    return success(code=200)

@manager.route("/<string:employee_id>/remove-manager/<string:manager_id>", methods=['GET'])  # type: ignore
def remove_manager(employee_id: str, manager_id: str) -> wrappers.Response:
    try:
        authClaims = checkPermission(request)
        manager = Manager(authClaims["uid"])
    except Exception:
        return failure(code=401)
    managerRemoved = manager.removeManagerForEmployee(employee_uid=employee_id, manager_uid=manager_id)
    return success(code=200) if managerRemoved is True else failure(code=400)

@manager.route("/<string:employee_id>/add-manager/<string:manager_id>", methods=['GET'])  # type: ignore
def add_manager(employee_id: str, manager_id: str) -> wrappers.Response:
    try:
        authClaims = checkPermission(request)
        manager = Manager(authClaims["uid"])
    except Exception:
        return failure(code=401)
    managerAdded = manager.assignOtherManager(employee_uid=employee_id, manager_uid=manager_id)
    return success(code=200) if managerAdded is True else failure(code=400)

@manager.route("/mark/<string:requestType>", methods=['POST'])  # type: ignore
def mark_leave(requestType: str) -> wrappers.Response:
    payload = request.json
    try:
        authClaims = checkPermission(request)
        manager = Manager(authClaims["uid"])
    except Exception:
        return failure(code=401)
    manager.markRequest(reqID=payload["reqID"], marked=payload["marked"])
    return success(code=200)

@manager.route("/get/<string:requestType>/<string:markedAs>", methods=['GET'])  # type: ignore
def get_leave(requestType: str, markedAs: str) -> wrappers.Response:
    try:
        authClaims = checkPermission(request)
        manager = Manager(authClaims["uid"])
    except Exception:
        return failure(code=401)
    reqs = []
    if markedAs == "pending":
        reqs = manager.getPendingRequests(reqType=requestType)
    else:
        reqs = manager.getMarkedRequests(reqType=requestType, markedAs=markedAs)
    return success(requestType, reqs, 200)
