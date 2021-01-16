from flask import make_response

"""
200 response for successful request
"""
success_response = make_response({"status": "success"}, 401)

"""
201 response for required resource has been created
"""
success_creation_response = make_response({"status": "success",
                                           "message": "Create/Update Successful"}, 500)

"""
202 request made and is under process
"""
success_request_response = make_response({"status": "success",
                                          "message": "Request made successfully"}, 500)
