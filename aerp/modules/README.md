Routes
======

/auth
-----
Contains Routes Related to Authentication and Signup

### 1. /auth/sign-user (POST request)

-   User SIGN in token verification and cookie creation in FE
-   Input json payload expected
    ```
    {
        "idToken" = "Firebasae ID token"
    }
    ```
-   Output json on Success 200
    ```
    {   "status" = "Success",
        user_details = {
            "access_token" = "timeLimitedAuthToken valid for 7 days",
            "email" = "user@email.com"
        }
    }
    ```

### 2. /auth/set-user-data (POST request)

-   Route to set user data for 1st time
-   Input json payload expected
    ```
    {
        "name" = "Some Dummy",
        "dob" = "yyyy-mm-dd",
        "phone" = "+1 1010101010",
        "personalEmail" = "email.example.com"
    }
    ```
-   Output json on Success 200
    ```
    {
        "status" = "Success",
        "user_id" = "some_user_id"
    }
    ```

### 3. /auth/sign-out (GET request)

-   Remove the HTTP only cookie for login
-   Output json on Success 200
    ```
    {
        "status" = "Success",
        "user_id" = "some_user_id"
    }
    ```

/employee
---------
Contains Routes that Permitted to all employees

`Note: Make sure to have the Authentication Header while making request or access_token Cookie in the FE`

### 1. /employee/info (GET request)

-   Get User Info
-   Output json on Success 200
    ```
    {
        "status" = "Success",
        "user_data" = {
            "user_id" = "User ID",
            "name" = "Name Name",
            "dob" = "yyyy-mm-dd",
            "phone" = "+100 1001001001",
            "email" = "abc@email.com",
            "personal_email" = "abc@mail.com",
            "role" = "SDE1",
            "team_id" = "MY TEAM",
            "team_name" = "MY TEAM NAME",
            "salary" = 101.00,
            "is_manager" = True,
            "manager_id" = "MAN ID",
            "manager_name" = "MAN NAME",
            "manager_email" = "mana@email.com",
            "payments" = [
                {
                    "date" = "yyyy-mm-dd",
                    "description" = "Some random Payment",
                    "amount" = 101.00,
                    "type" = "Debit"
                },
                {
                    "date" = "yyyy-mm-dd",
                    "description" = "Some other random Payment",
                    "amount" = 10.00,
                    "type" = "Credit"
                }
            ]
        }
    }
    ```

### 2. /employee/update-data (POST request)

-   Update the data that is accessable to all employees
-   Input json payload expected
    ```
    {
        "name" = "Name Name",
        "dob" = "yyyy-mm-dd",
        "phone" = "+100 1001001001"
        "personal_email" = "abc@mail.com"
    }
    ```
-   Output json on Success 200
    ```
    {
        "status" = "Success"
    }
    ```

### 3. /employee/create-leave (POST request)

-   Allows employees to request for leaves
-   Input json payload expected
    ```
    {
        "leave_start" = "yyyy-mm-dd",
        "leave_end" = "yyyy-mm-dd",
        "created" = "yyyy-mm-dd",
        "description" = "Some Random reason"
    }
    ```
-   Output json on Success 200
    ```
    {
        "status" = "Success"
    }
    ```

### 4. /employee/create-loan-raise-request (POST request)

-   Allows employees to request for leaves
-   Input json payload expected
    ```
    {
        "type" = "loan/raise",
        "amount" = 100.10,
        "created" = "yyyy-mm-dd",
        "description" = "Some Random reason"
    }
    ```
-   Output json on Success 200
    ```
    {
        "status" = "Success"
    }
    ```

### 5. /<string:reqType>/<string:markedAs> (GET request)

-   reqType can be one of "leave", "loan", "raise"
-   markedAs can be one of "pending", "accept", "reject"
-   Allows employees to get their requested leaves/loans/raise
-   Output json on Success 200
    ```
    {
        "status" = "Success",
        "loan" = {
            "created" = "2021-01-24",
            "creator_email" = "dganguly1120@gmail.com",
            "creator_id" = "0TXsyoWB2",
            "creator_name" = "Some Name",
            "description" = "Test",
            "leave_end" = "2021-01-25",
            "leave_id" = "0ToWB2-07LM",
            "leave_start" = "2021-01-25",
            "marked_as" = "pending",
            "marked_by_email" = "",
            "marked_by_name" = "",
            "marked_by_uid" = "",
            "type" = "leave"
        }
    }
    ```

Documentation for the rest is under Progress
