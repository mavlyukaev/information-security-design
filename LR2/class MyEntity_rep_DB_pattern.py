#import mysql.connector

class DBConnectionManager:
    _instance = None

    def __new__(cls, host, user, password, database):
        if cls._instance is None:
            cls._instance = super(DBConnectionManager, cls).__new__(cls)
            cls._instance._init_db_connection(host, user, password, database)
        return cls._instance

    def _init_db_connection(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def execute_query(self, query, params=None):
        """Выполняет SQL-запрос с параметрами."""
        self.cursor.execute(query, params)
        return self.cursor

    def commit(self):
        """Подтверждает транзакцию."""
        self.connection.commit()

    def __del__(self):
        """Закрывает соединение с БД."""
        self.cursor.close()
        self.connection.close()

class MyEntity_rep_DB:
    def __init__(self, host, user, password, database):
        # Инициализация через класс DBConnectionManager (одиночка)
        self.db_manager = DBConnectionManager(host, user, password, database)

    def get_by_id(self, driver_id):
        """Получить объект по ID"""
        query = "SELECT * FROM drivers WHERE DriverId = %s"
        cursor = self.db_manager.execute_query(query, (driver_id,))
        result = cursor.fetchone()
        return result

    def get_k_n_short_list(self, k, n):
        """Получить список k по счету n объектов класса short"""
        offset = (n - 1) * k
        query = "SELECT LastName, FirstName, Patronymic FROM drivers LIMIT %s OFFSET %s"
        cursor = self.db_manager.execute_query(query, (k, offset))
        results = cursor.fetchall()
        return results

    def add_entity(self, driver):
        """Добавить объект в список (при добавлении сформировать новый ID)"""
        query = """INSERT INTO drivers (LastName, FirstName, Patronymic, Experience) 
                   VALUES (%s, %s, %s, %s)"""
        self.db_manager.execute_query(query, (driver['LastName'], driver['FirstName'], driver['Patronymic'], driver['Experience']))
        self.db_manager.commit()
        return self.db_manager.cursor.lastrowid

    def replace_entity_by_id(self, driver_id, updated_driver):
        """Заменить элемент списка по ID"""
        query = """UPDATE drivers 
                   SET LastName = %s, FirstName = %s, Patronymic = %s, Experience = %s 
                   WHERE DriverId = %s"""
        self.db_manager.execute_query(query, (updated_driver['LastName'], updated_driver['FirstName'], updated_driver['Patronymic'], updated_driver['Experience'], driver_id))
        self.db_manager.commit()

    def delete_entity_by_id(self, driver_id):
        """Удалить элемент списка по ID"""
        query = "DELETE FROM drivers WHERE DriverId = %s"
        self.db_manager.execute_query(query, (driver_id,))
        self.db_manager.commit()

    def get_count(self):
        """Получить количество элементов"""
        query = "SELECT COUNT(*) as count FROM drivers"
        cursor = self.db_manager.execute_query(query)
        result = cursor.fetchone()
        return result['count'] if result else 0
