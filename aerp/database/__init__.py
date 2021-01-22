from firebase_admin import firestore, credentials, initialize_app
import os
import json

if os.environ.get("AERP_FIREBASE_CONFIG", None):
    creds_dict = json.loads(os.environ["AERP_FIREBASE_CONFIG"])
    db_credentials = credentials.Certificate(creds_dict)
else:
    db_credentials = credentials.Certificate("config/firebase_server.json")

firebase_default_app = initialize_app(db_credentials)
database = firestore.client(firebase_default_app)
