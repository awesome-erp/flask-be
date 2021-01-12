from typing import Optional, Any, Dict, List


def getUserLeaves(userID: str, user: Dict[str, Any], leaveType: str) -> List[Dict[str, Any]]:
    """
    Returns leaves of a particular type for all users

    Parameters
    ----------
    userID: str
        user ID
    profiles: Dict
        Dictionary with all user profiles
    leaveType: str
        Can be one of "pending_leaves"
                      ||"approved_leaves"
                      ||"cancelled_leaves"
                      ||"self_approved_leaves"
                      ||"self_rejected_leaves"

    Returns
    -------
    List[Dict[str, Any]]
        List with 
            uid: User id
            leave_id: str
            user_name: Name of employee
            leave_start: "dd-mm-yyyy"
            leave_end: "dd-mm-yyyy"
            leave_created: "dd-mm-yyyy"
            description: any notes related to the leaves
            markedBy: the manager who approved or rejected the leave
                      empty if not marked
    """
    leaveList = []
    for leaveID in user[leaveType]:
        leaveDict = user[leaveType][leaveID]
        modifiedLeaveDict = {
            "uid": userID,
            "leave_id": leaveID,
            "user_name": user["name"],
            "leave_start": leaveDict["leave_start"],
            "leave_end": leaveDict["leave_end"],
            "leave_created": leaveDict["leave_created"],
            "description": leaveDict["description"],
            "marked_by_uid": leaveDict["marked_by_uid"],
            "marked_by_name": leaveDict["marked_by_name"],
            "marked_by_email": leaveDict["marked_by_email"]
        }
        leaveList.append(modifiedLeaveDict)

    return leaveList


def getAllLeaves(database: Any, employees: List[str], leaveType: str) -> List[Dict[str, Any]]:
    """
    Returns leaves of a particular type for all employees in the list

    Parameters
    ----------
    database: Any
        user database
    employees: List[str] 
        It consists of all employee uids
    leaveType: str
        Can be "pending_leaves"||"approved_leaves"||"cancelled_leaves"

    Returns
    -------
    List[Dict[str, Any]]
        List of 
            uid: User id
            user_name: Name of employee
            leave_id: str
            leave_start: "dd-mm-yyyy"
            leave_end: "dd-mm-yyyy"
            leave_created: "dd-mm-yyyy"
            description: any notes related to the leaves
    """
    leaves = []
    for employee in employees:
        employeeDict = database.document(employee).get().to_dict()
        userLeaveList = getUserLeaves(employee, employeeDict, leaveType)
        leaves.extend(userLeaveList)
    
    return leaves
