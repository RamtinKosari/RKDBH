# - Import Configurations
from .Configs import *
from .Queries import *

##
# Holds Methods for Database Handling 
##
class DBHandler():
    # - Method to Initialize DBHandler Object 
    def __init__(
        self,
        _database: str = None,
        _password: str = None,
        _user: str = None,
        _host: str = None
    ):
        # - Database Cursor Object
        self.cursor = None
        # - Database Connection Object
        self.connection = None
        # - Connection Status
        self.connectionStatus = False
        # - Database Connection Parameters
        self.DBParameters = {
            "password": _password,
            "database": _database,
            "host": _host,
            "user": _user
        }
    # - Method to Connect to Database
    def connect(
        self,
        _auto_commit: bool = CONNECTION_AUTOCOMMIT,
        _database: str = None,
        _password: str = None,
        _user: str = None,
        _host: str = None
    ):
        try:
            # - Check id DBParameters are Set
            if self.DBParameters["database"] is None:
                # - Check if DB Parameters are Provided as Parameters
                if _database != None and _password != None and _user != None and _host != None:
                    # - Set DB Parameters
                    self.DBParameters = {
                        "password": _password,
                        "database": _database,
                        "host": _host,
                        "user": _user
                    }
                else:
                    if LOG_FAILURES:
                        print(DATABASE, FAILED, "Database Parameters are Missing")
                    return False
            # - Connect to Database
            self.connection = psycopg2.connect(**self.DBParameters)
            # - Set Auto Commit
            self.connection.autocommit = _auto_commit
            # - Create Cursor
            self.cursor = self.connection.cursor()
            # - Set Connection Status
            self.connectionStatus = True
            # - Print Connection Status
            if LOG_MESSAGES:
                print(DATABASE, SUCCESS, "Connected to the Database {}{}{}".format(INFO, self.DBParameters["database"], RESET))
            # - Disable Cursor Blinking
            if DISABLE_CURSOR_BLINKING:
                os.system("tput civis")
            # - Return True
            return True
        except Exception as e:
            if LOG_FAILURES:
                print(DATABASE, FAILED, "Can Not Connect to the Database {}{}{}".format(ERR, e, RESET))
            # - Set Connection Status
            self.connectionStatus = False
            # - Return False
            return False
    # - Method to Disconnect from Database
    def disconnect(self):
        try:
            # - Close Cursor
            self.cursor.close()
            # - Close Connection
            self.connection.close()
            # - Set Connection Status
            self.connectionStatus = True
            # - Print Disconnection Status
            if LOG_MESSAGES:
                print(DATABASE, SUCCESS, "Disconnected from the Database {}{}{}".format(INFO, self.DBParameters["database"], RESET))
            # - Return True
            return True
        except AttributeError as e:
            if LOG_FAILURES:
                print(DATABASE, FAILED, "Can Not Disconnect from the Database, Not Connected Already")
        except Exception as e:
            if LOG_FAILURES:
                print(DATABASE, FAILED, "Can Not Disconnect from the Database {}{}{}".format(ERR, e, RESET))
            # - Set Connection Status
            self.connectionStatus = False
            # - Return False
            return False