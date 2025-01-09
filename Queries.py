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
                init_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
                """,
                "galaxies": """
            CREATE TABLE galaxies (
                galaxy_id SERIAL PRIMARY KEY,
                galaxy_name VARCHAR(63) NOT NULL,
                distance_mpc INT NOT NULL,
                distance_ly INT NOT NULL,
                distance_km FLOAT NOT NULL,
                galaxy_mass INT DEFAULT NULL,
                constellation VARCHAR NOT NULL,
                galaxy_size INT DEFAULT NULL,
                galaxy_type int REFERENCES galaxy_types(type_id),
                discover_date TIMESTAMP DEFAULT NULL,
                description VARCHAR NOT NULL,
                declination FLOAT NOT NULL,
                right_ascension FLOAT NOT NULL,
                init_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
                """,
                "star_types": """
            CREATE TABLE star_types (
                type_id SERIAL PRIMARY KEY,
                type_name VARCHAR(63) NOT NULL,
                description VARCHAR DEFAULT NULL,
                typical_temp INT DEFAULT NULL,
                typical_radius INT DEFAULT NULL,
                typical_luminosity INT DEFAULT NULL,
                typical_mass INT DEFAULT NULL,
                typical_age INT DEFAULT NULL,
                init_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
                """,
                "stars": """
            CREATE TABLE stars (
                star_id SERIAL PRIMARY KEY,
                constellation VARCHAR NOT NULL,
                name VARCHAR(63) NOT NULL,
                mass FLOAT NOT NULL,
                radius FLOAT NOT NULL,
                luminosity FLOAT NOT NULL,
                spectral_type VARCHAR NOT NULL,
                temperature FLOAT NOT NULL,
                apparent_magnitude FLOAT NOT NULL,
                absolute_magnitude FLOAT NOT NULL,
                distance INT NOT NULL,
                rotation_velocity FLOAT NOT NULL,
                declination FLOAT NOT NULL,
                right_ascension FLOAT NOT NULL,
                discover_date TIMESTAMP DEFAULT NULL,
                is_variable BOOLEAN DEFAULT FALSE,
                init_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                galaxy_id int REFERENCES galaxies(galaxy_id),
                type int REFERENCES star_types(type_id)
            );
                """,
                "star_systems": """
            CREATE TABLE star_systems (
                system_id SERIAL PRIMARY KEY,
                name VARCHAR NOT NULL,
                number_of_stars INT DEFAULT 0,
                age FLOAT NOT NULL,
                distance INT NOT NULL,
                type_name VARCHAR DEFAULT NULL,
                first_star_id int REFERENCES stars(star_id),
                second_star_id int REFERENCES stars(star_id),
                third_star_id int REFERENCES stars(star_id),
                forth_star_id int REFERENCES stars(star_id),
                fifth_star_id int REFERENCES stars(star_id),
                init_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
                """,
                "planet_types": """
            CREATE TABLE planet_types (
                type_id SERIAL PRIMARY KEY,
                type_name VARCHAR(63) NOT NULL,
                description VARCHAR DEFAULT NULL,
                typical_mass FLOAT DEFAULT NULL,
                typical_radius FLOAT DEFAULT NULL,
                typical_temperature FLOAT DEFAULT NULL,
                typical_rotation_velocity FLOAT DEFAULT NULL,
                typical_rings BOOLEAN DEFAULT FALSE,
                typical_habitability BOOLEAN DEFAULT FALSE,
                typical_atmosphere VARCHAR DEFAULT NULL,
                init_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
                """,
                "planets": """
            CREATE TABLE planets (
                planet_id SERIAL PRIMARY KEY,
                name VARCHAR(63) NOT NULL,
                description VARCHAR DEFAULT NULL,
                mass FLOAT NOT NULL,
                radius FLOAT NOT NULL,
                luminosity_albedo FLOAT NOT NULL,
                orbital_period FLOAT NOT NULL,
                orbital_distance FLOAT NOT NULL,
                orbital_eccentricity FLOAT NOT NULL,
                orbital_inclination FLOAT NOT NULL,
                orbital_longitude FLOAT NOT NULL,
                orbital_periapsis FLOAT NOT NULL,
                orbital_apaapsis FLOAT NOT NULL,
                orbital_velocity FLOAT NOT NULL,
                rotation_period FLOAT NOT NULL,
                rotation_velocity FLOAT NOT NULL,
                planet_obliquity FLOAT NOT NULL,
                planet_temperature FLOAT NOT NULL,
                surface_temperature FLOAT NOT NULL,
                surface_pressure FLOAT NOT NULL,
                surface_gravity FLOAT NOT NULL,
                surface_water FLOAT NOT NULL,
                surface_land FLOAT NOT NULL,
                has_atmosphere BOOLEAN DEFAULT FALSE,
                has_rings BOOLEAN DEFAULT FALSE,
                has_moons BOOLEAN DEFAULT FALSE,
                has_life BOOLEAN DEFAULT FALSE,
                is_habitable BOOLEAN DEFAULT FALSE,
                density FLOAT NOT NULL,
                discover_date TIMESTAMP DEFAULT NULL,
                init_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                type int REFERENCES planet_types(type_id),
                system_id int REFERENCES star_systems(system_id)
            );
                """
            }
            # - Check if Table Query Exists
            if _table not in add_table_queries:
                return False
            # - Return Specific Query
            return add_table_queries[_table]