Awesome-ERP Backend([Click Here](https://github.com/awesome-erp/flask-be))
===============================
<p>
<img width="30%" style="padding: 5%; display: inline-block" src="/assets/aerp-color.svg">
<img width="30%" style="padding: 5%; display: inline-block" src="/assets/aerp-white.svg">
<img width="30%" style="padding: 5%; display: inline-block" src="/assets/aerp-black.svg">
</p>

Infrastructure
--------------

deployed at: https://awesome-erp-backend.herokuapp.com/

| Usecase     | Resource       |
|-------------|----------------|
| Backend     | [Flask](https://flask.palletsprojects.com/en/1.1.x/)|
| Database    | [Firebase](https://firebase.google.com/)|
| Lint        | [Zulint](https://github.com/zulip/zulint)|
| Deployment  | [Heroku](https://www.heroku.com/free)|


Project Structure
-----------------

```
║
╠══ aerp [The Main Project Directory]
║   ╠══ database [For all Database Utilities and Interactions]
║   ║   ╠══ models
║   ║   ║   ╠══ BaseModel.py [Prototype of a Model]
║   ║   ║   ╠══ Manager.py [Manager Level Functionalities]
║   ║   ║   ╚══ User.py [User Level Functionalities]
║   ║   ║
║   ║   ╠══ utils
║   ║   ║   ╠══ detailsExtraction.py [Functions to Filter Specific data from Piles of Useless Data]
║   ║   ║   ╚══ userDataValidity.py [Functions to Check Validity of Different Inputs to database]
║   ║   ║
║   ║   ╚══ __init__.py [Initialize the database]
║   ║
║   ╠══ modules [For Blueprints of Routes]
║   ║   ╠══ auth.py [Routes delivering Authentication Utilities]
║   ║   ╠══ employee.py [Routes delivering Employee Level Utilities]
║   ║   ╚══ manager.py [Routes delivering Manager Level Utilities]
║   ║
║   ╠══ utils [General Purpose Utils]
║   ║   ╠══ authorization.py [Functions Handling Auth Tokens]
║   ║   ╚══ responses.py [Predefined Response Types]
║   ║
║   ╚══ __init__.py [Initialize the App]
║
╠══ tools [The Utilities related to Deployment and Tests]
║   ╠══ custom_check.py [Defined Lint Rules]
║   ╠══ lint [The Main Lint Checker File]
║   ╠══ run-mypy [mypy rules file]
║   ╚══ set-env [Setup File for the Repository]
║
╠══ Config [The Configuration Files]
║   ╚══firebase_server.json [Optional can be passed with Environment Variables]
║
╠══ main.py [Starts Server]
╚══ requirements.txt
```

Deployment
----------

-   sudo apt update && sudo apt upgrade -y
-   Clone the repository `git clone https://github.com/awesome-erp/flask-be.git`
-   Install Dependencies `pip install -r requirements.txt`
-   Run Server from `app` in `main.py` Eg `python main.py`

Development
-----------

-   Fork the Repository
-   Clone the Fork `git clone https://github.com/`Github-User-Name`/flask-be.git`
-   Set upstream `git remote add upstream https://github.com/awesome-erp/flask-be.git`
-   Setup Environment `./tools/set-env`
-   Activate virtualenv
    -   Linux/OS X: `Source venv-awesome-erp/bin/activate`
    -   Windows WSL: `Source venv-awesome-erp/Scripts/activate`
-   Run Server `python3 main.py`<br>
    Good to Go:------------>
-   Make sure to run `./tools/lint` and get the tests passed before making commits

For More Docs:

-   [Database](/aerp/database/README.md)
-   [APIs](/aerp/modules/README.md)
