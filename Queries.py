class Queries:
    class Table:
        # - Find Element ID
        @staticmethod
        def FindID(__table, __column, __key_column, __key, __like = False):
            if __like == True and __key != None:
                __key = "%{}%".format(__key)
                if isinstance(__key, str):
                    __key = "'{}'".format(__key)
                return """
            SELECT {} FROM {} WHERE {} LIKE {}
                """.format(__column, __table, __key_column, __key)
            else:
                if isinstance(__key, str):
                    __key = "'{}'".format(__key)
                return """
            SELECT {} FROM {} WHERE {} = {}
                """.format(__column, __table, __key_column, __key)
        # - Update Value in Table
        @staticmethod
        def UpdateValue(__table, __column, __new, __column_key, __key):
            if isinstance(__key, str):
                __key = "'{}'".format(__key)
            if isinstance(__new, str):
                if __new == "NULL":
                    __new = "NULL"
                else:
                    __new = "'{}'".format(__new)
            return """
            UPDATE {} SET {} = {} WHERE {} = {};
            """.format(__table, __column, __new, __column_key, __key)
        # - Delete Value in Table
        @staticmethod
        def DeleteValue(__table, __column_key, __key):
            if isinstance(__key, str):
                __key = "'{}'".format(__key)
            return """
            DELETE FROM {} WHERE {} = {};
            """.format(__table, __column_key, __key)
        # - Add Table
        @staticmethod
        def Add(_table):
            # - Define Tables Queries
            add_table_queries = {
                "galaxy_types": """
            CREATE TABLE galaxy_types (
                type_id SERIAL PRIMARY KEY,
                type_name VARCHAR(63) NOT NULL,
                description VARCHAR NOT NULL,
                frequency FLOAT DEFAULT NULL,
                sub_type VARCHAR NOT NULL,
                avg_mass INT DEFAULT NULL,
                init_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            );
                """,
                # "galaxies": """
                # """,
                # "star_systems": """
                # """,
                # "star_types": """
                # """,
                # "stars": """
                # """,
                # "planet_types": """
                # """,
                # "planets": """
                # """
            }
            # - Check if Table Query Exists
            if _table not in add_table_queries:
                return False
            # - Return Specific Query
            return add_table_queries[_table]