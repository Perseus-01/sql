
# Создайте программу для управления клиентами на python.

# Требуется хранить персональную информацию о клиентах:

# имя
# фамилия
# email
# телефон
# Сложность в том, что телефон у клиента может быть не один, а два, три и даже больше. А может и вообще не быть телефона (например, он не захотел его оставлять).

# Вам необходимо разработать структуру БД для хранения информации и несколько функций на python для управления данными:

# Функция, создающая структуру БД (таблицы)
# Функция, позволяющая добавить нового клиента
# Функция, позволяющая добавить телефон для существующего клиента
# Функция, позволяющая изменить данные о клиенте
# Функция, позволяющая удалить телефон для существующего клиента
# Функция, позволяющая удалить существующего клиента
# Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)



import psycopg2

# conn - это коннект к базе
# для выполнения запросов нужен cursor

def create_db(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients(
                client_id SERIAL PRIMARY KEY,
                first_name VARCHAR(40),
                last_name VARCHAR(40),
                email VARCHAR(40) UNIQUE
            );
            """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS client_phone(
                client_id integer REFERENCES clients(client_id),
                phone VARCHAR(15)
            );
            """)
        cursor.commit()

def add_client(conn, first_name, last_name, email, phone=None):
    with conn.cursor() as cursor:
        cursor.execute("""
        INSERT INTO clients(first_name, last_name, email) VALUES(%s, %s, %s);
        
        """, (first_name, last_name, email))

    # если телефон будет указан, надо сделать еще один инсерт во вторую таблицу ???
    cursor.commit()

def add_phone(conn, client_id, phone):
    if phone is not None:
        with conn.cursor() as cursor:
            cursor.execute("""
        INSERT INTO client_phone(client_id, phone) VALUES(%s, %s);
        """, (client_id, phone))
            cursor.commit()

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    if first_name is not None:
        with conn.cursor() as cursor:
            cursor.execute("""
            UPDATE clients SET first_name=%s WHERE client_id=%s;
            """, (first_name, client_id))
            conn.execute("""
            SELECT * FROM clients;
            """)
        cursor.commit()
    
    if last_name is not None:
        cursor.execute("""
            UPDATE clients SET last_name=%s WHERE client_id=%s;
            """, (last_name, client_id))
        cursor.execute("""
            SELECT * FROM clients;
            """)
        cursor.commit()
    # по аналогии остальные, и, конечно, использовать cursor

def delete_phone(conn, client_id, phone):
    if phone is not None:
        with conn.cursor() as cursor:
            cursor.execute("""
        DELETE FROM client_phone WHERE client_id=%s AND phone LIKE %s;
        """, (client_id, phone))
            cursor.commit()

def delete_client(conn, client_id):
    with conn.cursor() as cursor:
        cursor.execute("""
        DELETE FROM clients WHERE id=%s;
        """, (1,))
        cursor.execute("""
        SELECT * FROM clients;
        """)
        cursor.commit()

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    if first_name is not None:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT c.client_id, c.first_name, c.last_name, c.email, p.phone FROM clients AS c
                LEFT JOIN client_phone AS cp ON c.client_id = cp.client_id
                WHERE c.first_name LIKE %s""", (first_name,))
        
            cursor.commit()



with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:
    # вызывайте функции здесь  #что указывать в параметрах?
    create_db(conn)
    # в функцию нужно передавать значения, ниже три примера
    add_client(conn, 'Ivan', 'Ivanov', 'ivan@mail.ru', phone='7777777777')
    add_client(conn, 'Ivan', 'Ivanov', 'ivan@mail.ru', '7777777777')
    add_client(conn, 'Ivan', 'Ivanov', email='ivan@mail.ru', phone='7777777777')
    add_phone(conn, 3, '78544678544')
    change_client(conn, 2, 'Petr', 'Petrov', 'petr@mail.ru', '33333333333')
    delete_phone(conn, 1, '7777777777777')
    delete_client(conn, 1)
    find_client(conn, 'Ivan', 'Ivanov', 'ivan.i@mail.ru', '7777777777777')


conn.close()