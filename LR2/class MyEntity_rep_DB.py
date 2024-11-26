import sqlite3

class MyEntity_rep_DB:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor(dictionary=True)

     def initialize_db(self):
        """Инициализация базы данных SQLite и создание таблицы drivers."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS drivers (
                DriverId INTEGER PRIMARY KEY AUTOINCREMENT,
                LastName TEXT NOT NULL,
                FirstName TEXT NOT NULL,
                Patronymic TEXT,
                Experience INTEGER NOT NULL
            )
        """)
        self.connection.commit()
        print("База данных SQLite и таблица 'drivers' успешно созданы.")

    def get_by_id(self, driver_id):
        """Получить объект по ID"""
        query = "SELECT * FROM drivers WHERE DriverId = %s"
        self.cursor.execute(query, (driver_id,))
        result = self.cursor.fetchone()
        if result:
            return result  # Вернуть как объект Driver или как словарь
        return None

    def get_k_n_short_list(self, k, n):
        """Получить список k по счету n объектов класса short"""
        offset = (n - 1) * k
        query = "SELECT LastName, FirstName, Patronymic FROM drivers LIMIT %s OFFSET %s"
        self.cursor.execute(query, (k, offset))
        results = self.cursor.fetchall()
        return results

    def add_entity(self, driver):
        """Добавить объект в список (при добавлении сформировать новый ID)"""
        query = """INSERT INTO drivers (LastName, FirstName, Patronymic, Experience) 
                   VALUES (%s, %s, %s, %s)"""
        self.cursor.execute(query, (driver['LastName'], driver['FirstName'], driver['Patronymic'], driver['Experience']))
        self.connection.commit()
        return self.cursor.lastrowid  # Новый ID

    def replace_entity_by_id(self, driver_id, updated_driver):
        """Заменить элемент списка по ID"""
        query = """UPDATE drivers 
                   SET LastName = %s, FirstName = %s, Patronymic = %s, Experience = %s 
                   WHERE DriverId = %s"""
        self.cursor.execute(query, (updated_driver['LastName'], updated_driver['FirstName'], updated_driver['Patronymic'], updated_driver['Experience'], driver_id))
        self.connection.commit()

    def delete_entity_by_id(self, driver_id):
        """Удалить элемент списка по ID"""
        query = "DELETE FROM drivers WHERE DriverId = %s"
        self.cursor.execute(query, (driver_id,))
        self.connection.commit()

    def get_count(self):
        """Получить количество элементов"""
        query = "SELECT COUNT(*) as count FROM drivers"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result['count'] if result else 0

    def __del__(self):
        """Закрыть соединение при уничтожении объекта"""
        self.cursor.close()
        self.connection.close()
