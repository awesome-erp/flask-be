from firebase_admin import auth
from flask import wrappers

def _cookieValid(request: wrappers.Request):
    return request.cookies.get("accessToken")

def _authorizationHeader(request: wrappers.Request):
    """method to extract token from the Authorization header"""
    return request.headers['authorization'].split(" ")[-1].strip()

def checkPermission(request: wrappers.Request):
    token = _cookieValid(request)
    if not token:
        token = _authorizationHeader(request)
    try:
        return auth.verify_session_cookie(token)
    except Exception:
        raise BaseException("Invalid access Token")
