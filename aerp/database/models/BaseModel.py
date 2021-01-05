from firebase_admin import firestore, credentials, initialize_app


class Base:
    """
    The base class model that extends to other models
    """
    def init_database(self) -> None:
        """
        Function for initialization of the database
        """
        # Get Firebase Certificate and Initialize Firebase database
        db_credentials = credentials.Certificate("config/firebase_server.json")
        firebase_default_app = initialize_app(db_credentials, {
            'storageBucket': 'anc-ang-dev-firebase.appspot.com'
        })

        database = firestore.client(firebase_default_app)
        return database
