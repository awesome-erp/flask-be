from firebase_admin import auth

def _cookieValid(request):
    return request.cookies.get("accessToken")

def _authorizationHeader(request):
    """method to extract token from the Authorization header"""
    return request.headers['authorization'].split(" ")[-1].strip()

def checkPermission(request):
    token = _cookieValid(request)
    print(token)
    if not token:
        token = _authorizationHeader(request)
        print(token)
    try:
        return auth.verify_session_cookie(token)
    except Exception:
        raise BaseException("Invalid access Token")
