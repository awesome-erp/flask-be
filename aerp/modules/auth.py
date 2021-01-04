from datetime import timedelta
from flask import Blueprint, make_response, request
from aerp.database.models.Users import User
from aerp.modules.utils.auth_utils import clearDataForSet


authorization = Blueprint("auth", __name__, static_folder='/static')


@authorization.route("/sign-user", methods=['POST'])
def sign_user():
    """
    Route for user SIGN in token verification
    """
    postData = request.json
    accessToken = postData["idToken"]
    try:
        user = User(accessToken)
    except Exception:
        response = {
            "status": "fail",
            "message": "ID token verification failed"
        }
        return make_response(response, 401)

    expiry = timedelta(days=7)
    timeLimitedAuthToken = user.getTimeLimitedToken(expiry=expiry)
    responseDict = {
        "status": "success",
        "accessToken": timeLimitedAuthToken
    }
    response = make_response(responseDict, 200)
    response.set_cookie('accessToken', timeLimitedAuthToken, secure=True,
                        httponly=True, samesite="Strict")

    return response


@authorization.route("/set-user-data", methods=['POST'])
def set_user_data():
    """
    Route to set user data for 1st time
    """
    postData = request.json
    accessToken = request.cookies.get("accessToken")
    try:
        user = User(accessToken)
    except Exception:
        response = {
            "status": "fail",
            "message": "ID token verification failed"
        }
        return make_response(response, 401)

    userPersonalData = clearDataForSet(postData)
    user.setData(**userPersonalData)
    responseDict = {
        "status": "success",
        "user_id": user.uid
    }
    return make_response(responseDict, 200)


@authorization.route("/userInfo", methods=['GET', 'POST'])
def user_info():
    """
    The Route to fetch and update user data

    GET
    ----
        Route to get user details
    POST
    ----
        Route to edit paricular user fields
    """
    accessToken = request.cookies.get("accessToken")
    try:
        user = User(accessToken)
    except Exception:
        response = {
            "status": "fail",
            "message": "ID token verification failed"
        }
        return make_response(response, 401)

    if request.method == "GET":
        user_profile = user.getData()
        return make_response(user_profile, 200)

    if request.method == "POST":
        postData = request.json
        name = None
        personal_email = None
        phone = None
        dob = None
        if "name" in postData:
            name = postData["name"]
        if "personal_email" in postData:
            personal_email = postData["personal_email"]
        if "phone" in postData:
            phone = postData["phone"]
        if "dob" in postData:
            dob = postData["dob"]
        try:
            user.updateUserEditableData(name=name,
                                        personal_email=personal_email,
                                        dob=dob, phone=phone)
            response = {
                "status": "success",
                "message": "user profile updated successfuly"
            }
        except Exception:
            response = {
                "status": "success",
                "message": "error updating user profile"
            }
        return make_response(response, 200)


@authorization.route("/sign-out", methods=['GET'])
def remCookie():
    resp = make_response({"status": "success"}, 200)
    resp.set_cookie('accessToken', '', expires=0,
                    secure=True, httponly=True, samesite="None")
    return resp
