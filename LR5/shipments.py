from models import MyEntityRepository, DBConnectionManager, Validator
import json
import yaml


class Shipment:
    """Класс Shipment полями из диаграммы и встроенной валидацией."""
    def __init__(self, shipment_id=None, route_id=None, driver_id=None,
                 departure_date=None, arrival_date=None, bonus=None):
        self.shipment_id = shipment_id
        self.route_id = Validator.validate_positive_integer(route_id, "ID маршрута")
        self.driver_id = Validator.validate_positive_integer(driver_id, "ID водителя")
        self.departure_date, self.arrival_date = Validator.validate_departure_and_arrival_dates(departure_date, arrival_date)
        self.bonus = Validator.validate_non_negative_number(bonus, "Премия")

    def __repr__(self):
        return (f"Shipment(shipment_id={self.shipment_id}, route_id={self.route_id}, driver_id={self.driver_id}, "
                f"departure_date={self.departure_date}, arrival_date={self.arrival_date}, bonus={self.bonus})")

    def __repr__(self):
        return (f"Shipment(shipment_id={self.shipment_id}, route_id={self.route_id}, driver_id={self.driver_id}, "
                f"departure_date={self.departure_date}, arrival_date={self.arrival_date}, bonus={self.bonus})")

class ShipmentsRepositoryJSON(MyEntityRepository):
    """Репозиторий для работы с перевозками в формате JSON."""
    def load_entities(self):
        """Загрузка данных из JSON-файла."""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Shipment(**entry) for entry in data]
        except FileNotFoundError:
            return []

    def save_entities(self):
        """Сохранение данных в JSON-файл."""
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([entity.__dict__ for entity in self.entities], file, ensure_ascii=False, indent=4)

class ShipmentsRepositoryYAML(MyEntityRepository):
    """Репозиторий для работы с перевозками в формате YAML."""
    def load_entities(self):
        """Загрузка данных из YAML-файла."""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file)
                return [Shipment(**entry) for entry in data]
        except FileNotFoundError:
            return []

    def save_entities(self):
        """Сохранение данных в YAML-файл."""
        with open(self.filename, "w", encoding="utf-8") as file:
            yaml.dump([entity.__dict__ for entity in self.entities], file, allow_unicode=True)

class ShipmentsRepositoryDB(MyEntityRepository):
    """Репозиторий для работы с таблицей shipments в базе данных."""
    def __init__(self, db_name):
        from models import DBConnectionManager
        self.db_manager = DBConnectionManager(db_name)
        self._initialize_table()

    def _initialize_table(self):
        """Создание таблицы, если её нет."""
        query = """
        CREATE TABLE IF NOT EXISTS shipments (
            ShipmentId INTEGER PRIMARY KEY AUTOINCREMENT,
            RouteId INTEGER NOT NULL,
            DriverId INTEGER NOT NULL,
            DepartureDate TEXT NOT NULL,
            ArrivalDate TEXT NOT NULL,
            Bonus INTEGER NOT NULL,
            FOREIGN KEY (RouteId) REFERENCES routes(RouteId),
            FOREIGN KEY (DriverId) REFERENCES drivers(DriverId)
        )
        """
        self.db_manager.execute_query(query)
        self.db_manager.commit()

    def get_by_id(self, shipment_id):
        """Получить перевозку по ID."""
        query = "SELECT * FROM shipments WHERE ShipmentId = ?"
        cursor = self.db_manager.execute_query(query, (shipment_id,))
        result = cursor.fetchone()
        if result:
            return Shipment(**result)
        return None

    def get_k_n_short_list(self, k, n):
        """Получить список k по счету n объектов класса Shipment."""
        offset = (k - 1) * n
        query = """
            SELECT ShipmentId, RouteId, DriverId, DepartureDate, ArrivalDate, Bonus
            FROM shipments
            LIMIT ? OFFSET ?
        """
        cursor = self.db_manager.execute_query(query, (n, offset))
        results = cursor.fetchall()
        return [Shipment(**dict(row)) for row in results]

    def add_entity(self, shipment):
        """Добавить перевозку в базу данных."""
        query = """
        INSERT INTO shipments (RouteId, DriverId, DepartureDate, ArrivalDate, Bonus)
        VALUES (?, ?, ?, ?, ?)
        """
        self.db_manager.execute_query(query, (
            Validator.validate_positive_integer(shipment.route_id, "ID маршрута"),
            Validator.validate_positive_integer(shipment.driver_id, "ID водителя"),
            Validator.validate_date(shipment.departure_date, "Дата отправления"),
            Validator.validate_date(shipment.arrival_date, "Дата прибытия"),
            Validator.validate_bonus(shipment.bonus, "Премия"),
        ))
        self.db_manager.commit()

    def replace_entity_by_id(self, shipment_id, updated_shipment):
        """Обновить перевозку по ID."""
        query = """UPDATE shipments SET RouteId = ?, DriverId = ?, DepartureDate = ?, 
                   ArrivalDate = ?, Bonus = ? WHERE ShipmentId = ?"""
        self.db_manager.execute_query(query, (updated_shipment.route_id, updated_shipment.driver_id,
                                              updated_shipment.departure_date, updated_shipment.arrival_date,
                                              updated_shipment.bonus, shipment_id))
        self.db_manager.commit()

    def delete_entity_by_id(self, shipment_id):
        """Удалить перевозку по ID."""
        query = "DELETE FROM shipments WHERE ShipmentId = ?"
        self.db_manager.execute_query(query, (shipment_id,))
        self.db_manager.commit()

    def get_count(self):
        """Получить количество перевозок."""
        query = "SELECT COUNT(*) FROM shipments"
        cursor = self.db_manager.execute_query(query)
        result = cursor.fetchone()
        return result[0] if result else 0