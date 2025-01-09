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
        # - Query Object
        self.query = Queries()
        # - List of Tables that Flagged as Error
        self.errorTables = []
        # - List of Tables that Flagged as Success
        self.successTables = []
        # - List of Tables that Flagged as Existing
        self.existingTables = []
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
            # self.cursor.close()
            # - Close Connection
            # self.connection.close()
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
    # - Method to Execute Query
    def execQuery(self, _query: str, _flow_queries: bool = False):
        try:
            # - Check if Connection is Established
            if self.connectionStatus == False:
                # - Connect to The Database
                self.connect()
                if LOG_FAILURES:
                    print(DATABASE, FAILED, "Can Not Execute Query, Connection is Not Established")
                # - Return Result
                return results
            # - Execute Query
            self.cursor.execute(_query)
            # - Get Results
            results = self.cursor.fetchall()
            # - Disconnect After Query Execution
            if DISCONNECT_AFTER_QUERY_EXECUTION:
                self.disconnect()
            # - Return Results
            return results
        except Exception as e:
            # - Check if No Results to Fetch
            if "no results to fetch" in str(e):
                # - Disconnect from Database if Not in Flow Queries Mode
                if _flow_queries == False:
                    print("ssssssss")
                    self.disconnect()
                # - Return status
                return True
            # - Log Failure
            if LOG_FAILURES:
                print(DATABASE, FAILED, "Can Not Execute Query :\n{}{}{}\nError : {}{}".format(INFO, _query, ERR, e, RESET))
            # - Return False
            return False
    # - Method to Check if Table Exists
    def checkTable(self, table_name):
        # - Check Connection Status
        if self.connectionStatus == False:
            # - Connect to The Database
            self.connect()
            # - Check Connection Status
            if self.connectionStatus == False:
                return False
        # - Check if Table Exists
        try:
            self.cursor.execute("SELECT * FROM information_schema.tables WHERE table_name = '{}'".format(table_name))
            # - Get Result
            result = self.cursor.fetchall()
            # - Check if Table Exists
            if len(result) == 0:
                # - Show Log
                # print(DATABASE, WARNING, "Table {}{}{} Does Not Exist".format(INFO, table_name, RESET))
                # - Disconnect from Database
                self.disconnect()
                # - Return False
                return False
            # - Disconnect from Database
            self.disconnect()
            # - Return True
            return True
        except Exception as err:
            # - Show Log
            print(DATABASE, FAILED, "Can Not Check Table, Error :\n{}{}{}".format(ERR, err, RESET), end = '')
            # - Disconnect from Database
            self.disconnect()
            # - Return Error
            return False
    # - Method to Add Table
    def addTable(self, table_name: str, _add_multiple_tables: bool = False):
        # - Check if Table Already Exists
        if self.checkTable(table_name):
            # - Show Log
            print(DATABASE, WARNING, "Table {}{}{} Already Exists".format(INFO, table_name, RESET),)
            # - Return True
            return True
        # - Set Table Query
        try:
            query = self.query.Table.Add(table_name)
            # - Check Query
            if query == False:
                # - Show Log
                print(DATABASE, FAILED, "Can Not Add Table {}{}{}, Because its Query is Not Defined".format(ERR, table_name, RESET), end = '',)
                # - Set Table to Existing Tables
                self.existingTables.append(table_name)
                # - Return False
                return False
            # - Add Table
            try:
                self.execQuery(query, _add_multiple_tables)
                # - Check if Table Exists
                if self.checkTable(table_name):
                    # - Show Log
                    print(DATABASE, SUCCESS, "Added Table {}{}{} :\n{}{}{}".format(INFO, table_name, RESET, INFO, query, RESET),)
                    # - Add Table to Success Tables
                    self.successTables.append(table_name)
                    # - Return True
                    return True
                else:
                    # - Show Log
                    print(DATABASE, FAILED, "Can Not Add Table {}{}{}".format(ERR, table_name, RESET), end = '',)
                    # - Add Table to Error Tables
                    self.errorTables.append(table_name)
                    # - Return False
                    return False
            except Exception as e:
                # - Show Log
                print(DATABASE, FAILED, "Can Not Add Table, Error :\n{}{}{}".format(ERR, e, RESET), end = '',)
                # - Add Table to Error Tables
                self.errorTables.append(table_name)
                # - Return Error
                return False
        except Exception as e:
            # - Show Log
            print(DATABASE, FAILED, "Can Not Add Table that Its Query is Not Defined, Error :\n{}{}{}".format(ERR, e, RESET), end = '',)
            # - Return Error
            return False
    # - Method to Drop Table
    def dropTable(self, table_name):
        # - Check Connection Status
        if self.connectionStatus == False:
            # - Connect to The Database
            self.connect()
            # - Check Connection Status
            if self.connectionStatus == False:
                return False
        # - Check if Table Exists
        if not self.checkTable(table_name):
            # - Show Log
            print(DATABASE, WARNING, "Table {}{}{} Does Not Exist".format(INFO, table_name, RESET),)
            # - Disconnect from Database
            self.disconnect()
            # - Return True
            return True
        # - Drop Table
        try:
            self.cursor.execute("DROP TABLE IF EXISTS {}".format(table_name))
            # - Show Log
            print(DATABASE, SUCCESS, "Dropped Table {}{}{}".format(INFO, table_name, RESET),)
            # - Disconnect from Database
            self.disconnect()
            # - Return True
            return True
        except Exception as err:
            # - Show Log
            print(DATABASE, FAILED, "Can Not Drop Table, Error :\n{}{}{}".format(ERR, err, RESET), end = '', force = True)
            # - Disconnect from Database
            self.disconnect()
            # - Return Error
            return False
    # - Method to Add All Tables
    def addAllTables(self):
        # - Check Connection Status
        if self.connectionStatus == False:
            # - Connect to The Database
            self.connect()
            # - Check Connection Status
            if self.connectionStatus == False:
                return False
        # - Show Log
        print(DATABASE, "Adding All Tables ...")
        # - Sort Tables by Their Order
        sorted_tables = dict(sorted(DB_TABLES.items(), key = lambda item: item[1]))
        order_counter = 0
        for table, order in sorted_tables.items():
            order_counter += 1
            if order < 9:
                print("{}0{} -> {}".format(INFO, order + 1, table))
            else:
                print("{}{} -> {}".format(INFO, order + 1, table))
        # - Add Tables
        count_of_added_tables = 0
        for table, order in sorted_tables.items():
            if self.addTable(table, True) == True:
                count_of_added_tables += 1