import sqlite3

class Model:
    def __init__(self, db_name="database.db"):
        self.connection = sqlite3.connect(db_name)
        self.connection.row_factory = sqlite3.Row  # Позволяет доступ по ключам
        self.cursor = self.connection.cursor()
        self._initialize_table()

    def _initialize_table(self):
        try:
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
        except sqlite3.Error as e:
            print(f"Ошибка при инициализации таблицы: {e}")

    def get_all_records(self):
        try:
            self.cursor.execute("SELECT DriverId, LastName, FirstName, Experience FROM drivers")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Ошибка при получении записей: {e}")
            return []

    def get_record_by_id(self, record_id):
        try:
            self.cursor.execute("SELECT * FROM drivers WHERE DriverId = ?", (record_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Ошибка при получении записи по ID: {e}")
            return None

    def add_record(self, last_name, first_name, patronymic, experience):
        try:
            self.cursor.execute(
                "INSERT INTO drivers (LastName, FirstName, Patronymic, Experience) VALUES (?, ?, ?, ?)",
                (last_name, first_name, patronymic, experience)
            )
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Ошибка при добавлении записи: {e}")
            self.connection.rollback()

    def update_record(self, record_id, last_name, first_name, patronymic, experience):
        try:
            record_id = int(record_id)  # Преобразуем ID в число для безопасности
            self.cursor.execute(
                "UPDATE drivers SET LastName = ?, FirstName = ?, Patronymic = ?, Experience = ? WHERE DriverId = ?",
                (last_name, first_name, patronymic, experience, record_id)
            )
            self.connection.commit()
        except Exception as e:
            print(f"Ошибка при обновлении записи: {e}")
            self.connection.rollback()


    def delete_record(self, record_id):
        try:
            self.cursor.execute("DELETE FROM drivers WHERE DriverId = ?", (record_id,))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Ошибка при удалении записи: {e}")
            self.connection.rollback()

    def close_connection(self):
        """Закрытие соединения с базой данных"""
        self.connection.close()

    def __del__(self):
        """Уничтожение объекта и закрытие соединения"""
        self.close_connection()
