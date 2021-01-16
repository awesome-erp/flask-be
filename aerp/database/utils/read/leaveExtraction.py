from typing import Any, Dict, List, Generator

def getAllLeaves(leaves: Generator) -> List[Dict[str, Any]]:
    """
    Returns leaves of a particular type for all employees in the list

    Parameters
    ----------
    employees: Generator
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
    leavesList = []
    for leave in leaves:
        print(type(leave))
        leaveDict = leave.to_dict()
        leavesList.append(leaveDict)

    return leavesList
