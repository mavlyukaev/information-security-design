import sqlite3

class DBConnectionManager:
    _instance = None

    def __new__(cls, db_name="drivers.db"):
        if cls._instance is None:
            cls._instance = super(DBConnectionManager, cls).__new__(cls)
            cls._instance._init_db_connection(db_name)
        return cls._instance

    def _init_db_connection(self, db_name):
        """Инициализация соединения SQLite"""
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._initialize_table()

    def _initialize_table(self):
        """Создание таблицы drivers, если её нет"""
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

    def execute_query(self, query, params=None):
        """Выполняет SQL-запрос с параметрами."""
        if params is None:
            params = ()
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
    def __init__(self, db_name="drivers.db"):
        # Инициализация через класс DBConnectionManager (одиночка)
        self.db_manager = DBConnectionManager(db_name)

    def get_by_id(self, driver_id):
        """Получить объект по ID"""
        query = "SELECT * FROM drivers WHERE DriverId = ?"
        cursor = self.db_manager.execute_query(query, (driver_id,))
        result = cursor.fetchone()
        return result

    def get_k_n_short_list(self, k, n):
        """Получить список k по счету n объектов"""
        offset = (k - 1) * n
        query = "SELECT LastName, FirstName, Patronymic FROM drivers LIMIT ? OFFSET ?"
        cursor = self.db_manager.execute_query(query, (k, offset))
        results = cursor.fetchall()
        return results

    def add_entity(self, driver):
        """Добавить объект в базу данных"""
        query = """INSERT INTO drivers (LastName, FirstName, Patronymic, Experience) 
                   VALUES (?, ?, ?, ?)"""
        self.db_manager.execute_query(query, (driver['LastName'], driver['FirstName'], driver['Patronymic'], driver['Experience']))
        self.db_manager.commit()
        return self.db_manager.cursor.lastrowid

    def replace_entity_by_id(self, driver_id, updated_driver):
        """Обновить элемент по ID"""
        query = """UPDATE drivers 
                   SET LastName = ?, FirstName = ?, Patronymic = ?, Experience = ? 
                   WHERE DriverId = ?"""
        self.db_manager.execute_query(query, (updated_driver['LastName'], updated_driver['FirstName'], updated_driver['Patronymic'], updated_driver['Experience'], driver_id))
        self.db_manager.commit()

    def delete_entity_by_id(self, driver_id):
        """Удалить объект по ID"""
        query = "DELETE FROM drivers WHERE DriverId = ?"
        self.db_manager.execute_query(query, (driver_id,))
        self.db_manager.commit()

    def get_count(self):
        """Получить количество объектов"""
        query = "SELECT COUNT(*) FROM drivers"
        cursor = self.db_manager.execute_query(query)
        result = cursor.fetchone()
        return result[0] if result else 0
