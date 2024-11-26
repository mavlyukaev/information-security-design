class DBRepositoryAdapter(MyEntityRepository):
    def __init__(self, host, user, password, database):
        super().__init__(None)  # filename здесь не нужен
        self.db_manager = DBConnectionManager(host, user, password, database)

    def load_entities(self):
        """Загрузка данных из базы — адаптируем под общий интерфейс"""
        query = "SELECT * FROM drivers"
        cursor = self.db_manager.execute_query(query)
        results = cursor.fetchall()
        return [Driver(**row) for row in results]

    def save_entities(self):
        """Сохранение данных не реализуется, так как операции выполняются напрямую через методы"""
        pass

    def get_by_id(self, driver_id):
        """Получить объект по ID через DBConnectionManager"""
        query = "SELECT * FROM drivers WHERE DriverId = %s"
        cursor = self.db_manager.execute_query(query, (driver_id,))
        result = cursor.fetchone()
        if result:
            return Driver(**result)
        return None

    def add_entity(self, driver):
        """Добавить объект в базу данных"""
        query = """INSERT INTO drivers (LastName, FirstName, Patronymic, Experience)
                   VALUES (%s, %s, %s, %s)"""
        self.db_manager.execute_query(query, (driver.LastName, driver.FirstName, driver.Patronymic, driver.Experience))
        self.db_manager.commit()

    def replace_entity_by_id(self, driver_id, updated_driver):
        """Обновить объект в базе данных"""
        query = """UPDATE drivers SET LastName = %s, FirstName = %s, Patronymic = %s, Experience = %s
                   WHERE DriverId = %s"""
        self.db_manager.execute_query(query, (
            updated_driver.LastName,
            updated_driver.FirstName,
            updated_driver.Patronymic,
            updated_driver.Experience,
            driver_id
        ))
        self.db_manager.commit()

    def delete_entity_by_id(self, driver_id):
        """Удалить объект по ID"""
        query = "DELETE FROM drivers WHERE DriverId = %s"
        self.db_manager.execute_query(query, (driver_id,))
        self.db_manager.commit()

    def get_count(self):
        """Получить количество объектов"""
        query = "SELECT COUNT(*) as count FROM drivers"
        cursor = self.db_manager.execute_query(query)
        result = cursor.fetchone()
        return result['count'] if result else 0
