from flask import make_response, wrappers
from typing import Any

def success(key: str = "", value: Any = "", code: int = 200) -> wrappers.Response:

    responseDict = {"status": "Success"}
    if key != "" and value != "":
        responseDict[key] = value
    return make_response(responseDict, code)

def failure(key: str = "", value: Any = "", code: int = 401) -> wrappers.Response:

    responseMessages = {401: "ID token verification failed",
                        400: "Internal Error",
                        500: "Internal Server Error"}
    responseDict = {"status": "Failure",
                    "message": responseMessages[code]}
    if key != "" and value != "":
        responseDict[key] = value
    return make_response(responseDict, code)
