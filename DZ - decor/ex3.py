from ex1 import logger
import psycopg2

with psycopg2.connect(database='netology_db', user='postgres', password='99113322vfrcbv') as conn:
    @logger
    def add_client(cur, name: str, last_name: str, email: str):
        cur.execute("""
            INSERT INTO clients(name, last_name, email) VALUES (%s, %s, %s);
        """, (name, last_name, email,))
        return

    with conn.cursor() as cur:

        add_client(cur, 'Юра', 'Младенцев', 'nagibator@mail.ru')
