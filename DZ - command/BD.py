import psycopg2


with psycopg2.connect(database='command_work', user='postgres', password='99113322vfrcbv') as conn:
    with conn.cursor() as cur:
        cur.execute("""
                    DROP TABLE IF EXISTS user_info;
                    DROP TABLE IF EXISTS elect_users;
                    DROP TABLE IF EXISTS info_elect;
            """)
        cur.execute("""
                CREATE TABLE IF NOT EXISTS user_info(
                    user_id SERIAL PRIMARY KEY,
                    first_name VARCHAR(32) NOT NULL,
                    last_name VARCHAR(32) NOT NULL,
                    link VARCHAR(64) UNIQUE,
                    sex VARCHAR(32),
                    age INTEGER,
                    city VARCHAR(64)
                );
        """)
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS elect_users(
                        el_user_id SERIAL PRIMARY KEY,
                        first_name VARCHAR(64),
                        last_name VARCHAR(64),
                        link VARCHAR(64) UNIQUE,
                        sex VARCHAR(32),
                        age INTEGER,
                        city VARCHAR(64)
                    );
        """)
        cur.execute("""
                CREATE TABLE IF NOT EXISTS info_elect(
                    user_id INTEGER REFERENCES user_info(user_id),
                    el_user_id INTEGER REFERENCES elect_users(el_user_id),
                    CONSTRAINT inf_elect PRIMARY KEY (user_id, el_user_id)
                    );
        """)
