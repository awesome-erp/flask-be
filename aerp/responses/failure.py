from flask import make_response, wrappers

"""
401 response for Authentication Failure
"""
auth_failure_response = make_response({"status": "failure",
                                                 "message": "ID token verification failed"}, 401)
def custom_auth_failure_response(field: str, value: Any) -> wrappers.Response:
    return make_response({"status": "failure", field: value}, 401)
"""
500 Internal Server Error
"""
internal_server_error_response = make_response({"status": "failure",
                                                "message": "Internal Server Errror"}, 500)
