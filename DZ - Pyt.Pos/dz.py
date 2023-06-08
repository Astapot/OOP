import psycopg2

with psycopg2.connect(database='netology_db', user='postgres', password='99113322vfrcbv') as conn:

    # Задание 2
    def add_client(cur, name: str, last_name: str, email: str):
        cur.execute("""
            INSERT INTO clients(name, last_name, email) VALUES (%s, %s, %s);
        """, (name, last_name, email,))
        return

    # Задание 3. Сделал через 2 функции. Сначала нахожу айдишник по имени и фамилии, потом используя айди добавляю
        # номер телефона. Правильнее было сделать через емайл, поскольку он уникальный, а имя фамилия нет, но я сделал так,
        # потому что мне показалось это удобнее для пользователя. Учел, что клиента может не быть через трай ексепт.


    def find_id(cur, name, last_name):
        cur.execute("""
                       SELECT client_id
                       FROM clients
                       WHERE name = %s and last_name = %s;
        """, (name, last_name,))

        try:
            return cur.fetchone()[0]
        except TypeError:
            return 'Такого клиента нет'

    def add_number(cur, name, last_name, telephone):
        id = find_id(cur, name, last_name)
        if type(id) == int:
            cur.execute("""
                           INSERT INTO client_tel(client_id, telephone) VALUES (%s, %s) RETURNING tel_id;
                   """, (id, telephone))
            return cur.fetchone()
        return id

    # Задание 4. Использовал функцию из 3 задания. Сделал 2 варианта, просто потому что захотелось, второй вариант
    # конечно правильнее. Но, как мне кажется все равно для пользователя тяжеловат.

    def update_client(cur, name, last_name):
        id = find_id(cur, name, last_name)
        if type(id) == int:
            new_name = input('Введите новое имя: ')
            new_last_name = input('Введите новую фамилию: ')
            new_email = input('Введите новый email: ')
            cur.execute("""
                               UPDATE clients SET name = %s WHERE client_id = %s;       
                           """, (new_name, id,))
            cur.execute("""
                               UPDATE clients SET last_name = %s WHERE client_id = %s;       
                           """, (new_last_name, id,))
            cur.execute("""
                               UPDATE clients SET email = %s WHERE client_id = %s;       
                           """, (new_email, id,))
            return id
        return id

    def update_client_2(cur, name, last_name, new_name, new_last_name, new_email):
        id = find_id(cur, name, last_name)
        if type(id) == int:
            cur.execute("""
                               UPDATE clients SET name = %s WHERE client_id = %s;       
                           """, (new_name, id,))
            cur.execute("""
                               UPDATE clients SET last_name = %s WHERE client_id = %s;       
                           """, (new_last_name, id,))
            cur.execute("""
                               UPDATE clients SET email = %s WHERE client_id = %s;       
                           """, (new_email, id,))
            return id
        return id


    # Задание 5 Дополнительная функция находит все номера по клиенту.


    def find_telephones(cur, id):
        cur.execute("""
                           SELECT telephone
                           FROM client_tel
                           WHERE client_id = %s;
            """, (id,))
        tuple_tel = cur.fetchall()
        if len(tuple_tel) > 0:
            array_tel = []
            for i in tuple_tel:
                for k in i:
                    array_tel.append(k)
            return array_tel
        return 'телефонный номер не зарегистрирован'


    def delete_number(cur, name, last_name, telephone):
        id = find_id(cur, name, last_name)
        if type(id) == int:
            tels = find_telephones(cur, id)
            if telephone in tels:
                cur.execute("""
                                DELETE FROM client_tel WHERE telephone = %s and client_id = %s;                
                """, (telephone, id,))
                return 'Успешно'
            return 'Введен неверный номер'
        return id


    # Задание 6

    def delete_client(cur, name, last_name):
        id = find_id(cur, name, last_name)
        if type(id) == int:
            cur.execute("""
                            DELETE FROM client_tel WHERE client_id = %s;
                            DELETE FROM clients WHERE client_id = %s;
            """, (id, id,))
            return f'{name} {last_name} удален успешно'
        return id


    # Задание 7. Похожая функция уже есть, можно было ее в самом начале использовать вместо find_id
    # Учел что у пользователя могут быть одинаковые данные
    # Старая версия, ниже новая

    def find_client(cur, name=None, last_name=None, email=None, telephone=None):
        if telephone is None:
            cur.execute("""
                                    SELECT * FROM clients WHERE name = %s OR last_name = %s OR email = %s;            
                    """, (name, last_name, email,))
            client_info = cur.fetchall()
            if len(client_info) > 0:
                for i in client_info:
                    id = i[0]
                    info = i[1:]
                    cur.execute("""
                                    SELECT telephone FROM client_tel WHERE client_id = %s
                    """, (id,))
                    numbers = find_telephones(cur, id)
                    print(f'Имя: {info[0]}, фамилия: {info[1]}, email: {info[2]}, telephones: {numbers}')
                return '.'

        else:
            cur.execute("""
                            SELECT client_id FROM client_tel WHERE telephone = %s;
            """, (telephone,))
            client_info = cur.fetchall()
            if len(client_info) > 0:
                id = client_info[0][0]
                cur.execute("""
                                SELECT name, last_name, email FROM clients WHERE client_id = %s;            
                                """, (id,))
                info = cur.fetchone()
                numbers = find_telephones(cur, id)
                return f'Имя: {info[0]}, фамилия: {info[1]}, email: {info[2]}, telephones: {numbers}'
        return 'Такого клиента нет'

    # Задание 7. Новая версия


    def find_client2(cur, name='NULL', last_name='NULL', email='NULL', telephone='NULL'):
        cur.execute("""
                                            SELECT c.client_id, name, last_name, email, telephone FROM clients c
                                            FULL JOIN client_tel ct ON c.client_id = ct.client_id
                                            WHERE (c.name = %s OR %s = %s) AND (c.last_name = %s OR %s = %s)
                                            AND (c.email = %s OR %s = %s) AND (ct.telephone = %s OR %s = %s)           
                            """, (name, name, 'NULL', last_name, last_name, 'NULL', email, email, 'NULL', telephone, telephone, 'NULL'))
        client_info = cur.fetchall()
        if len(client_info) > 0:
            id = client_info[0][0]
            cur.execute("""
                            SELECT name, last_name, email FROM clients WHERE client_id = %s;            
                            """, (id,))
            info = cur.fetchone()
            numbers = find_telephones(cur, id)
            return f'Имя: {info[0]}, фамилия: {info[1]}, email: {info[2]}, telephones: {numbers}'
        return 'Такого клиента нет'

    with conn.cursor() as cur:

        # Задание 1. Поскольку нигде не сказано, решил делать все задания при условии уникальности пары имя, фамилия.
        # Если надо переделать напишите, емайл все равно уникальный можно было через него, подумал для пользователя так
        # удобнее

        cur.execute("""
                    DROP TABLE IF EXISTS client_tel;
                    DROP TABLE IF EXISTS clients;
            """)
        cur.execute("""
                CREATE TABLE IF NOT EXISTS clients(
                    client_id SERIAL PRIMARY KEY,
                    name VARCHAR(32) NOT NULL,
                    last_name VARCHAR(32) NOT NULL,
                    email VARCHAR(64) UNIQUE
                );
        """)
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS client_tel(
                        tel_id SERIAL PRIMARY KEY,
                        client_id INTEGER REFERENCES clients(client_id),
                        telephone VARCHAR(64)
                    );
            """)




















        # add_client(cur, 'Юра', 'Младенцев', 'nagibator@mail.ru')
        # add_client(cur, 'ЖЖЖ', 'ЫЫЫ', 'sss@mail.ru')
        # add_client(cur, '1', '5', '123123@mail.ru')
        # add_client(cur, 'Антон', 'Антон', 'anton@mail.ru')
        # add_client(cur, 'Антон', 'Коля', 'kolant@mail.ru')
        # add_client(cur, 'Коля', 'Коля', 'kolya@mail.ru')
        # add_client(cur, 'Инвокер', 'Пуджевич', '322@yandex.ru')
        # add_client(cur, 'Буханка', 'Хлебов', 'yandex@mail.ru')
        # add_number(cur, 'Юра', 'Младенцев', '88005553535')
        # add_number(cur, 'Юра', 'Младенцев', '88005553537')
        # add_number(cur, 'Коля', 'Коля', '88005553539')
        # add_number(cur, 'Коля', 'Коля', '8800')
        # add_number(cur, 'ЖЖЖ', 'ЫЫЫ', '555')
        # add_number(cur, 'ЖЖЖ', 'ЫЫЫ', '111')
        # add_number(cur, 'ЖЖЖ', 'ЫЫЫ', '999')
        # add_number(cur, 'Юра', 'Младенцев', '8908908090')
        # add_number(cur, 'Инвокер', 'Пуджевич', '123654')
        #
        # find_id(cur, 'Андрей', 'Младенцев')
        # print(add_number(cur, 'Андрей', 'Младенцев', '89009090909'))
        # add_number(cur, 'Юра', 'Младенцев', '88005553536')
        # add_number(cur, 'Инвокер', 'Пуджевич', '322')
        # add_number(cur, 'Инвокер', 'Пуджевич', '322-322')
        # add_number(cur, 'Буханка', 'Хлебов', '123456789')
        #
        # # в функции update_client используется инпут, будьте внимательны!
        # # print(update_client(cur, 'Юра', 'Младенцев'))
        #
        # update_client_2(cur, 'Юра', 'Младенцев', 'Максим', 'Младенцев', '123')
        #
        # find_telephones(cur, 3)
        # delete_number(cur, 'Инвокер', 'Пуджевич', '322')
        # delete_number(cur, 'Инвокер', 'Пуджевич', '111')
        # delete_number(cur, 'Инвокер', 'Младенцев', '111')
        #
        # print(delete_client(cur, 'Максим', 'Младенцев'))
        # print(delete_client(cur, 'Юрец', 'Младенцев'))
        # print(find_client(cur, name='Инвокер'))
        # print(find_client(cur, telephone='322-322'))
        # print(find_client(cur, last_name='Коля'))
        # print(find_client(cur, last_name='Антон'))
        # print(find_client(cur, last_name='Анто'))
        # print(find_client2(cur, last_name='ЫЫЫ'))
        # print(find_client2(cur, last_name='Пуджевич', name='Инвокер'))
        # print(find_client2(cur, last_name='Пуджевич', name='Юрий'))
        # print(find_client2(cur, telephone='111'))
        # print(find_client2(cur, name='Антон', last_name='Коля'))

#     conn.commit()
# conn.close()

