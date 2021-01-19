from aerp.database import database


class Base:
    """
    The base class model that extends to other models
    """
    def init_database(self) -> None:
        """
        Function for initialization of the databases
        """
        self.database = database.collection("user_profiles")
        self.requests_database = database.collection("requests")

