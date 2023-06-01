import psycopg2

conn = psycopg2.connect(database='netology_db', user='postgres', password='99113322vfrcbv')
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




    # Задание 2



    def add_client(name: str, last_name: str, email: str):
        cur.execute("""
            INSERT INTO clients(name, last_name, email) VALUES (%s, %s, %s);
        """, (name, last_name, email,))
        return




    # Задание 3. Сделал через 2 функции. Сначала нахожу айдишник по имени и фамилии, потом используя айди добавляю
    # номер телефона. Правильнее было сделать через емайл, поскольку он уникальный, а имя фамилия нет, но я сделал так,
    # потому что мне показалось это удобнее для пользователя. Учел, что клиента может не быть через трай ексепт.


    def find_id(name, last_name):
        cur.execute("""
                       SELECT client_id
                       FROM clients
                       WHERE name = %s and last_name = %s;
        """, (name, last_name,))

        try:
            return cur.fetchone()[0]
        except TypeError:
            return 'Такого клиента нет'

    def add_number(name, last_name, telephone):
        id = find_id(name, last_name)
        if type(id) == int:
            cur.execute("""
                           INSERT INTO client_tel(client_id, telephone) VALUES (%s, %s) RETURNING tel_id;
                   """, (id, telephone))
            return cur.fetchone()
        return id



    # Задание 4. Использовал функцию из 3 задания. Сделал 2 варианта, просто потому что захотелось, второй вариант
    # конечно правильнее. Но, как мне кажется все равно для пользователя тяжеловат.


    def update_client(name, last_name):
        id = find_id(name, last_name)
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

    def update_client_2(name, last_name, new_name, new_last_name, new_email):
        id = find_id(name, last_name)
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


    def find_telephones(id):
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


    def delete_number(name, last_name, telephone):
        id = find_id(name, last_name)
        if type(id) == int:
            tels = find_telephones(id)
            if telephone in tels:
                cur.execute("""
                                DELETE FROM client_tel WHERE telephone = %s and client_id = %s;                
                """, (telephone, id,))
                return 'Успешно'
            return 'Введен неверный номер'
        return id



    # Задание 6


    def delete_client(name, last_name):
        id = find_id(name, last_name)
        if type(id) == int:
            cur.execute("""
                            DELETE FROM client_tel WHERE client_id = %s;
                            DELETE FROM clients WHERE client_id = %s;
            """, (id, id,))
            return f'{name} {last_name} удален успешно'
        return id





    # Задание 7. Похожая функция уже есть, можно было ее в самом начале использовать вместо find_id
    # Учел что у пользователя могут быть одинаковые данные


    def find_client(name=None, last_name=None, email=None, telephone=None):
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
                    numbers = find_telephones(id)
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
                numbers = find_telephones(id)
                return f'Имя: {info[0]}, фамилия: {info[1]}, email: {info[2]}, telephones: {numbers}'
        return 'Такого клиента нет'





    # add_client('Юра', 'Младенцев', 'nagibator@mail.ru')
    # add_client('ЖЖЖ', 'ЫЫЫ', 'sss@mail.ru')
    # add_client('1', '5', '123123@mail.ru')
    # add_client('Антон', 'Антон', 'anton@mail.ru')
    # add_client('Антон', 'Коля', 'kolant@mail.ru')
    # add_client('Коля', 'Коля', 'kolya@mail.ru')
    # add_client('Инвокер', 'Пуджевич', '322@yandex.ru')
    # add_client('Буханка', 'Хлебов', 'yandex@mail.ru')
    # add_number('Юра', 'Младенцев', '88005553535')
    # add_number('Юра', 'Младенцев', '88005553537')
    # add_number('Коля', 'Коля', '88005553539')
    # add_number('Коля', 'Коля', '8800')
    # add_number('ЖЖЖ', 'ЫЫЫ', '555')
    # add_number('ЖЖЖ', 'ЫЫЫ', '111')
    # add_number('ЖЖЖ', 'ЫЫЫ', '999')
    # add_number('Юра', 'Младенцев', '8908908090')
    # add_number('Инвокер', 'Пуджевич', '123654')

    # find_id('Андрей', 'Младенцев')
    # print(add_number('Андрей', 'Младенцев', '89009090909'))
    # add_number('Юра', 'Младенцев', '88005553536')
    # add_number('Инвокер', 'Пуджевич', '322')
    # add_number('Инвокер', 'Пуджевич', '322-322')
    # add_number('Буханка', 'Хлебов', '123456789')

    # в функции update_client используется инпут, будьте внимательны!
    # print(update_client('Юра', 'Младенцев'))

    # update_client_2('Юра', 'Младенцев', 'Максим', 'Младенцев', '123')
    #
    # find_telephones(3)
    # delete_number('Инвокер', 'Пуджевич', '322')
    # delete_number('Инвокер', 'Пуджевич', '111')
    # delete_number('Инвокер', 'Младенцев', '111')

    # print(delete_client('Максим', 'Младенцев'))
    # print(delete_client('Юрец', 'Младенцев'))
    # print(find_client(name='Инвокер'))
    # print(find_client(telephone='322-322'))
    # print(find_client(last_name='Коля'))
    # print(find_client(last_name='Антон'))
    # print(find_client(last_name='Анто'))
    conn.commit()
conn.close()

