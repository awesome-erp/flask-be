from firebase_admin import firestore, credentials, initialize_app


class Base:

    def init_database(self):

        # Get Firebase Certificate and Initialize Firebase database
        db_credentials = credentials.\
                         Certificate("config/firebase_server.json")
        firebase_default_app = initialize_app(db_credentials, {
            'storageBucket': 'anc-ang-dev-firebase.appspot.com'
        })

        database = firestore.client(firebase_default_app)
        return database