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
                "days": """
            CREATE TABLE days (
                id SERIAL PRIMARY KEY,
                -- | Main Details
                summary TEXT NOT NULL,
                tags TEXT[],
                tasks TEXT[],
                projects TEXT[],
                projects_tasks TEXT[],
                rate INT CHECK (rate BETWEEN 0 AND 10),
                mood VARCHAR(50) CHECK (mood IN (
                    'Happy', 'Sad', 'Excited', 'Tired', 
                    'Stressed', 'Relaxed', 'Angry', 'Neutral'
                )),
                weather VARCHAR(50) CHECK (weather IN (
                    'Sunny', 'Cloudy', 'Rainy', 'Stormy', 
                    'Snowy', 'Windy', 'Foggy', 'Clear Night'
                )),
                sleep_hours DECIMAL(3,1) CHECK (sleep_hours BETWEEN 0 AND 24),
                sleep_quality DECIMAL(3,1) CHECK (sleep_quality BETWEEN 0 AND 10),
                people_met TEXT[],
                places_met TEXT[],
                achievements TEXT[],
                challenges TEXT[],
                productivity DECIMAL(3,1) CHECK (productivity BETWEEN 0 AND 10),
                income DECIMAL(10,2),
                expenses DECIMAL(10,2),
                entertainments TEXT[],
                social_media TEXT[],
                social_media_time DECIMAL(3,1) CHECK (social_media_time BETWEEN 0 AND 24),
                hydration DECIMAL(3,1) CHECK (hydration BETWEEN 0 AND 10),
                screen_time DECIMAL(3,1) CHECK (screen_time BETWEEN 0 AND 24),
                work_hours DECIMAL(3,1) CHECK (work_hours BETWEEN 0 AND 24),
                study_hours DECIMAL(3,1) CHECK (study_hours BETWEEN 0 AND 24),
                biggest_lesson TEXT,
                musics TEXT[],
                new_ideas TEXT[],
                -- | Health Details
                self_care_details TEXT[],
                health_issues TEXT[],
                meals TEXT[],
                breakfast TEXT[],
                lunch TEXT[],
                dinner TEXT[],
                snacks TEXT[],
                blood_pressure VARCHAR(50) CHECK (blood_pressure IN (
                    'Low', 'Normal', 'High', 'Very High'
                )),
                heart_rate INT,
                weight DECIMAL(5,2),
                height DECIMAL(5,2),
                bmi DECIMAL(5,2),
                outdoor_time DECIMAL(3,1) CHECK (outdoor_time BETWEEN 0 AND 24),
                dreams TEXT[],
                masturbation BOOLEAN DEFAULT FALSE,
                dance BOOLEAN DEFAULT FALSE,
                -- | Time Details
                date DATE,
                start TIMESTAMP,
                end TIMESTAMP,
                -- | Workout Details
                workout_id INT REFERENCES workouts(id),
                -- | Location Details
                location_id INT REFERENCES locations(id),
                -- | Self Care Details
                hidden BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT NOW()
            );
                """,
                "locations": """
            CREATE TABLE locations (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                address VARCHAR(255),
                city VARCHAR(255),
                category VARCHAR(255),
                lat FLOAT,
                lng FLOAT,
                created_at TIMESTAMP DEFAULT NOW()
            );
                """,
                "workouts": """
            CREATE TABLE workouts (
                id SERIAL PRIMARY KEY,
                -- | Main Details
                day_id INT REFERENCES days(id),
                type TEXT,
                details TEXT,
                -- | Workout Details
                intensity DECIMAL(3,1) CHECK (intensity BETWEEN 0 AND 10),
                calories DECIMAL(5,2),
                heart_rate INT,
                -- | Time Details
                start TIMESTAMP,
                end TIMESTAMP,
                duration DECIMAL(3,1) CHECK (duration BETWEEN 0 AND 24),
                -- Walking Details
                distance DECIMAL(5,2) DEFAULT 0,
                speed DECIMAL(5,2) DEFAULT 0,
                steps INT DEFAULT 0,
                -- Self Care Details
                hidden BOOLEAN DEFAULT FALSE,
                musics TEXT[],
                created_at TIMESTAMP DEFAULT NOW()
            );
                """,
                "tags": """
            CREATE TABLE tags (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                description TEXT,
                color VARCHAR(50),
                created_at TIMESTAMP DEFAULT NOW()
            );
                """,
                "projects": """
            CREATE TABLE projects (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                description TEXT,
                category VARCHAR(255),
                tags TEXT[],
                tasks TEXT[],
                project_id INT,
                created_at TIMESTAMP DEFAULT NOW()
            );
                """,
                "tasks": """
            CREATE TABLE tasks (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                description TEXT,
                category VARCHAR(255),
                tags TEXT[],
                created_at TIMESTAMP DEFAULT NOW()
            );
                """,
                "people": """
            CREATE TABLE people (
                id SERIAL PRIMARY KEY,
                fullname VARCHAR(255),
                age INT,
                address VARCHAR(255),
                city VARCHAR(255),
                country VARCHAR(255),
                email VARCHAR(255),
                phone VARCHAR(255),
                social_media TEXT[],
                gender VARCHAR(255),
                height DECIMAL(5,2),
                weight DECIMAL(5,2),
                bmi DECIMAL(5,2),
                blood_type VARCHAR(50),
                birth_date DATE,
                birth_place VARCHAR(255),
                occupation VARCHAR(255),
                education VARCHAR(255),
                relationship_status VARCHAR(255),
                status_update_time TIMESTAMP,
                nationality VARCHAR(255),
                nationality_code VARCHAR(255),
                languages TEXT[],
                interests TEXT[],
                skills TEXT[],
                driving_license BOOLEAN DEFAULT FALSE,
                driving_license_type VARCHAR(255),
                driving_license_issue_date DATE,
                driving_license_expiry_date DATE,
                passport BOOLEAN DEFAULT FALSE,
                passport_number VARCHAR(255),
                passport_issue_date DATE,
                passport_expiry_date DATE,
                visa BOOLEAN DEFAULT FALSE,
                health_issues TEXT[],
                description TEXT,
                relationship VARCHAR(255),
                total_time_spent DECIMAL(3,1),
                total_meetings INT,
                tags TEXT[],
                created_at TIMESTAMP DEFAULT NOW()
            );
                """,
                "places": """
            CREATE TABLE places (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                address VARCHAR(255),
                city VARCHAR(255),
                country VARCHAR(255),
                category VARCHAR(255),
                lat FLOAT,
                lng FLOAT,
                tags TEXT[],
                number_of_visits INT,
                total_time_spent DECIMAL(3,1),
                description TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            );
                """,
                "achievements": """
            CREATE TABLE achievements (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                description TEXT,
                category VARCHAR(255),
                tags TEXT[],
                points INT CHECK (points BETWEEN 0 AND 100),
                created_at TIMESTAMP DEFAULT NOW()
            );
                """,
                "challenges": """
            CREATE TABLE challenges (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                description TEXT,
                category VARCHAR(255),
                tags TEXT[],
                rate INT CHECK (rate BETWEEN 0 AND 100),
                how_tackled TEXT,
                status VARCHAR(50) CHECK (status IN (
                    'Not Started', 'In Progress', 'Completed', 'Failed'
                )),
                difficulty VARCHAR(50) CHECK (difficulty IN (
                    'Easy', 'Medium', 'Hard', 'Very Hard'
                )),
                reward TEXT,
                comments TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            );
                """,
                "musics": """
            CREATE TABLE musics (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                artist VARCHAR(255),
                album VARCHAR(255),
                genre VARCHAR(255),
                tags TEXT[],
                duration DECIMAL(3,1),
                release_date DATE,
                rate INT CHECK (rate BETWEEN 0 AND 10),
                language VARCHAR(255),
                is_favorite BOOLEAN DEFAULT FALSE,
                number_of_plays INT,
                created_at TIMESTAMP DEFAULT NOW()
            );
                """,
                "meals": """
            CREATE TABLE meals (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                description TEXT,
                category VARCHAR(255),
                tags TEXT[],
                ingredients TEXT[],
                recipe TEXT,
                calories DECIMAL(5,2),
                protein DECIMAL(5,2),
                fat DECIMAL(5,2),
                carbohydrates DECIMAL(5,2),
                sugar DECIMAL(5,2),
                fiber DECIMAL(5,2),
                cholesterol DECIMAL(5,2),
                sodium DECIMAL(5,2),
                potassium DECIMAL(5,2),
                calcium DECIMAL(5,2),
                iron DECIMAL(5,2),
                vitamins TEXT[],
                rate INT CHECK (rate BETWEEN 0 AND 10),
                is_favorite BOOLEAN DEFAULT FALSE,
                number_of_servings INT,
                preparation_time DECIMAL(3,1),
                cooking_time DECIMAL(3,1),
                created_at TIMESTAMP DEFAULT NOW()
            );
                """,
                "entertainments": """
            CREATE TABLE entertainments (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                description TEXT,
                category VARCHAR(255),
                count INT,
                tags TEXT[],
                rate INT CHECK (rate BETWEEN 0 AND 10),
                created_at TIMESTAMP DEFAULT NOW()
            );
                """,
                "social_media": """
            CREATE TABLE social_media (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                description TEXT,
                tags TEXT[],
                rate INT CHECK (rate BETWEEN 0 AND 10),
                total_time_spent DECIMAL(3,1),
                usage_count INT,
                created_at TIMESTAMP DEFAULT NOW()
            );
                """,
                "health_issues": """
            CREATE TABLE health_issues (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                description TEXT,
                category VARCHAR(255),
                tags TEXT[],
                symptoms TEXT[],
                treatment_plan TEXT,
                medication TEXT[],
                start_date DATE,
                end_date DATE,
                status VARCHAR(50) CHECK (status IN (
                    'In Progress', 'Completed'
                )),
                doctor_notes TEXT,
                rate INT CHECK (rate BETWEEN 0 AND 10),
                created_at TIMESTAMP DEFAULT NOW()
            );
                """,
                "self_care": """
            CREATE TABLE self_care (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                description TEXT,
                category VARCHAR(255),
                tags TEXT[],
                duration DECIMAL(3,1),
                frequency VARCHAR(50) CHECK (frequency IN (
                    'Daily', 'Weekly', 'Monthly', 'Yearly'
                )),
                benefits TEXT,
                instructions TEXT,
                rate INT CHECK (rate BETWEEN 0 AND 10),
                created_at TIMESTAMP DEFAULT NOW()
            );
                """,
                "biggest_lessons": """
            CREATE TABLE biggest_lessons (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                description TEXT,
                category VARCHAR(255),
                tags TEXT[],
                rate INT CHECK (rate BETWEEN 0 AND 10),
                created_at TIMESTAMP DEFAULT NOW()
            );
                """,
                "new_ideas": """
            CREATE TABLE new_ideas (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                description TEXT,
                category VARCHAR(255),
                tags TEXT[],
                rate INT CHECK (rate BETWEEN 0 AND 10),
                implementation_status VARCHAR(50) CHECK (implementation_status IN (
                    'Not Started', 'In Progress', 'Completed', 'Failed'
                )),
                impacts TEXT[],
                feasibility VARCHAR(50) CHECK (feasibility IN (
                    'Low', 'Medium', 'High', 'Very High'
                )),
                risks TEXT[],
                priority_level INT CHECK (priority_level BETWEEN 0 AND 10),
                required_resources TEXT[],
                created_at TIMESTAMP DEFAULT NOW()
            );
                """,
                "dreams": """
            CREATE TABLE dreams (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                description TEXT,
                timestamp TIMESTAMP,
                symbolic_meaning TEXT, -- Like Water, Fire, Earth, Air
                interpretation TEXT,
                type VARCHAR(50) CHECK (type IN (
                    'Lucid Dream', 'Nightmare', 'Recurring Dream', 'Daydream', 'Normal'
                )),
                mood_before_sleep VARCHAR(50) CHECK (mood_before_sleep IN (
                    'Happy', 'Sad', 'Excited', 'Tired', 
                    'Stressed', 'Relaxed', 'Angry', 'Neutral'
                )),
                mood_after_sleep VARCHAR(50) CHECK (mood_after_sleep IN (
                    'Happy', 'Sad', 'Excited', 'Tired', 
                    'Stressed', 'Relaxed', 'Angry', 'Neutral'
                )),
                tags TEXT[],
                sleep_quality DECIMAL(3,1) CHECK (sleep_quality BETWEEN 0 AND 10),
                sleep_duration DECIMAL(3,1) CHECK (sleep_duration BETWEEN 0 AND 24),
                sleep_time TIME,
                wake_up_time TIME,
                possible_triggers TEXT[],
                rate INT CHECK (rate BETWEEN 0 AND 10),
                created_at TIMESTAMP DEFAULT NOW()
            );
                """
            }
            # - Check if Table Query Exists
            if _table not in add_table_queries:
                return False
            # - Return Specific Query
            return add_table_queries[_table]