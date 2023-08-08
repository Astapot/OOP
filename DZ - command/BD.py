import psycopg2

class PostgresUser:
    def __init__(self, database, user, password):
        self.database = database
        self.user = user
        self.password = password

current_user = PostgresUser('command_work', 'postgres', '99113322vfrcbv')
def add_user(user_id, first_name, last_name, sex, age, city, number=0):
    with psycopg2.connect(database=current_user.database, user=current_user.user, password=current_user.password) as conn:
        with conn.cursor() as cur:
            check_user_in_db = find_id(user_id)
            if not check_user_in_db:
                cur.execute("""
                           INSERT INTO user_info(user_id, first_name, last_name, sex, age, city) VALUES (%s, %s, %s, %s, %s, %s);
                       """, (user_id, first_name, last_name, sex, age, city,))
                cur.execute("""
                            INSERT INTO user_number(user_id, number) VALUES (%s, %s);
                                           """, (user_id, number,))
        return

def find_id(user_id):
    with psycopg2.connect(database=current_user.database, user=current_user.user, password=current_user.password) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                           SELECT user_id
                           FROM user_info
                           WHERE user_id = %s;
            """, (user_id,))
            try:
                return cur.fetchone()[0]
            except TypeError:
                return False

def find_elect_id(el_user_id, user_id):
    with psycopg2.connect(database=current_user.database, user=current_user.user, password=current_user.password) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT eu.first_name, eu.last_name, eu.link FROM elect_users eu
                        LEFT JOIN info_elect ie ON eu.el_user_id = ie.el_user_id
                        LEFT JOIN user_info ui ON ie.user_id = ui.user_id
                        WHERE eu.el_user_id = %s AND ui.user_id = %s
            """, (el_user_id, user_id,))
            try:
                return cur.fetchone()[0]
            except TypeError:
                return False

def add_to_behind_rel(cur, user_id, el_user_id):
    cur.execute("""
                INSERT INTO info_elect(user_id, el_user_id) VALUES (%s, %s);
    """, (user_id, el_user_id))

def add_elect_user(user_id, el_user_id, first_name, last_name, link, sex, city):
    with psycopg2.connect(database=current_user.database, user=current_user.user, password=current_user.password) as conn:
        with conn.cursor() as cur:
            check_el_user_in_db = find_elect_id(el_user_id, user_id)
            if not check_el_user_in_db:
                cur.execute("""
                        INSERT INTO elect_users(el_user_id, first_name, last_name, link, sex, city) VALUES (%s, %s, %s, %s, %s, %s);
                """, (el_user_id, first_name, last_name, link, sex, city))
                add_to_behind_rel(cur, user_id, el_user_id)
            return check_el_user_in_db

def give_all_elect_users(user_id):
    with psycopg2.connect(database=current_user.database, user=current_user.user, password=current_user.password) as conn:
        with conn.cursor() as cur:
            check_user_in_db = find_id(user_id)
            if check_user_in_db:
                cur.execute("""
                            SELECT eu.first_name, eu.last_name, eu.link FROM elect_users eu
                            LEFT JOIN info_elect ie ON eu.el_user_id = ie.el_user_id
                            LEFT JOIN user_info ui ON ie.user_id = ui.user_id
                            WHERE ui.user_id = %s;                                 
                """, (user_id,))
                result = cur.fetchall()
                if len(result) == 0:
                    return 'no users'
                else:
                    return result
            else:
                return False

def update_number(user_id, number):
    with psycopg2.connect(database=current_user.database, user=current_user.user, password=current_user.password) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                            UPDATE user_number SET number = %s WHERE user_id = %s;       
                                       """, (number, user_id,))

def get_number(user_id):
    with psycopg2.connect(database=current_user.database, user=current_user.user, password=current_user.password) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT number
                        FROM user_number
                        WHERE user_id = %s;
            """, (user_id,))
            return cur.fetchone()


with psycopg2.connect(database=current_user.database, user=current_user.user, password=current_user.password) as conn:
    with conn.cursor() as cur:
        # cur.execute("""
        #             DROP TABLE IF EXISTS info_elect;
        #             DROP TABLE IF EXISTS user_info;
        #             DROP TABLE IF EXISTS elect_users;
        #     """)
        cur.execute("""
                CREATE TABLE IF NOT EXISTS user_info(
                    user_id SERIAL PRIMARY KEY,
                    first_name VARCHAR(32) NOT NULL,
                    last_name VARCHAR(32) NOT NULL,
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
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS user_number(
                            user_id INTEGER REFERENCES user_info(user_id),
                            number INTEGER
                            );
                """)

