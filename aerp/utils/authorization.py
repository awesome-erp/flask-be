from firebase_admin import auth
from flask.wrappers import Request
from typing import Dict, Optional

def _cookieValid(request: Request) -> Optional[str]:
    return request.cookies.get("accessToken")

def _authorizationHeader(request: Request) -> Optional[str]:
    """method to extract token from the Authorization header"""
    return request.headers['authorization'].split(" ")[-1].strip()

def checkPermission(request: Request) -> Dict[str, str]:
    token = _cookieValid(request)
    if not token:
        token = _authorizationHeader(request)
    try:
        return auth.verify_session_cookie(token)
    except Exception:
        raise BaseException("Invalid access Token")
