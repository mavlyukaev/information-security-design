from models import MyEntityRepository, DBConnectionManager, Validator
import json
import yaml


class Route:
    """Класс Route полями из диаграммы и встроенной валидацией."""
    def __init__(self, route_id=None, route_name=None, start_route=None, end_route=None,
                 distance=None, driver_payment=None):
        self.route_id = route_id
        self.route_name = Validator.validate_string(route_name, "Название маршрута")
        self.start_route = Validator.validate_string(start_route, "Начальная точка")
        self.end_route = Validator.validate_string(end_route, "Конечная точка")
        self.distance = Validator.validate_positive_integer(distance, "Расстояние")
        self.driver_payment = Validator.validate_positive_integer(driver_payment, "Оплата водителю")

    def __repr__(self):
        return (f"Route(route_id={self.route_id}, route_name={self.route_name}, start_route={self.start_route}, "
                f"end_route={self.end_route}, distance={self.distance}, driver_payment={self.driver_payment})")


class RoutesRepositoryJSON(MyEntityRepository):
    """Репозиторий для работы с маршрутами в формате JSON."""
    def load_entities(self):
        """Загрузка данных из JSON-файла."""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Route(**entry) for entry in data]
        except FileNotFoundError:
            return []

    def save_entities(self):
        """Сохранение данных в JSON-файл."""
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([entity.__dict__ for entity in self.entities], file, ensure_ascii=False, indent=4)

class RoutesRepositoryYAML(MyEntityRepository):
    """Репозиторий для работы с маршрутами в формате YAML."""
    def load_entities(self):
        """Загрузка данных из YAML-файла."""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file)
                return [Route(**entry) for entry in data]
        except FileNotFoundError:
            return []

    def save_entities(self):
        """Сохранение данных в YAML-файл."""
        with open(self.filename, "w", encoding="utf-8") as file:
            yaml.dump([entity.__dict__ for entity in self.entities], file, allow_unicode=True)


class RoutesRepositoryDB(MyEntityRepository):
    """Репозиторий для работы с таблицей routes в базе данных."""
    def __init__(self, db_name):
        from models import DBConnectionManager
        self.db_manager = DBConnectionManager(db_name)
        self._initialize_table()

    def _initialize_table(self):
        """Создание таблицы, если её нет."""
        query = """
        CREATE TABLE IF NOT EXISTS routes (
            RouteId INTEGER PRIMARY KEY AUTOINCREMENT,
            RouteName TEXT NOT NULL,
            StartRoute TEXT NOT NULL,
            EndRoute TEXT NOT NULL,
            Distance INTEGER NOT NULL,
            DriverPayment INTEGER NOT NULL
        )
        """
        self.db_manager.execute_query(query)
        self.db_manager.commit()

    def get_by_id(self, route_id):
        """Получить маршрут по ID."""
        query = "SELECT * FROM routes WHERE RouteId = ?"
        cursor = self.db_manager.execute_query(query, (route_id,))
        result = cursor.fetchone()
        if result:
            return Route(**result)
        return None

    def get_k_n_short_list(self, k, n):
        """Получить список k по счету n объектов класса Route."""
        offset = (k - 1) * n
        query = """
            SELECT RouteId, RouteName, StartRoute, EndRoute, Distance, DriverPayment
            FROM routes
            LIMIT ? OFFSET ?
        """
        cursor = self.db_manager.execute_query(query, (n, offset))
        results = cursor.fetchall()
        return [Route(**dict(row)) for row in results]

    def add_entity(self, route: Route):
        """Добавить маршрут в базу данных."""
        query = """INSERT INTO routes (RouteName, StartRoute, EndRoute, Distance, DriverPayment)
                   VALUES (?, ?, ?, ?, ?)"""
        self.db_manager.execute_query(query, (
            route.route_name, route.start_route, route.end_route, route.distance, route.driver_payment
        ))
        self.db_manager.commit()

    def replace_entity_by_id(self, route_id, updated_route):
        """Обновить маршрут по ID."""
        query = """UPDATE routes SET RouteName = ?, StartRoute = ?, EndRoute = ?, 
                   Distance = ?, DriverPayment = ? WHERE RouteId = ?"""
        self.db_manager.execute_query(query, (updated_route.route_name, updated_route.start_route,
                                              updated_route.end_route, updated_route.distance,
                                              updated_route.driver_payment, route_id))
        self.db_manager.commit()

    def delete_entity_by_id(self, route_id):
        """Удалить маршрут по ID."""
        query = "DELETE FROM routes WHERE RouteId = ?"
        self.db_manager.execute_query(query, (route_id,))
        self.db_manager.commit()

    def get_count(self):
        """Получить количество маршрутов."""
        query = "SELECT COUNT(*) FROM routes"
        cursor = self.db_manager.execute_query(query)
        result = cursor.fetchone()
        return result[0] if result else 0