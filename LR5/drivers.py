from models import MyEntityRepository, DBConnectionManager, Validator
import json
import yaml


class Driver:
    """Класс Driver с полями из диаграммы и встроенной валидацией."""

    def __init__(self, driver_id=None, last_name=None, first_name=None, patronymic=None, birthday=None,
                 phone_number=None, driver_license=None, vehicle_title=None, insurance_policy=None,
                 license_plate=None, experience=None):
        self.driver_id = driver_id
        self.last_name = Validator.validate_string(last_name, "Фамилия")
        self.first_name = Validator.validate_string(first_name, "Имя")
        self.patronymic = Validator.validate_string(patronymic, "Отчество")
        self.birthday = Validator.validate_date(birthday, "Дата рождения")
        self.phone_number = Validator.validate_phone_number(phone_number, "Номер телефона")
        self.driver_license = Validator.validate_license(driver_license, "Водительское удостоверение")
        self.vehicle_title = Validator.validate_license(vehicle_title, "ПТС")
        self.insurance_policy = Validator.validate_policy(insurance_policy, "Страховой полис")
        self.license_plate = Validator.validate_license_plate(license_plate, "Номер машины")
        self.experience = Validator.validate_positive_integer(experience, "Стаж")

    def __repr__(self):
        return (f"Driver(driver_id={self.driver_id}, last_name='{self.last_name}', first_name='{self.first_name}', "
                f"patronymic='{self.patronymic}', birthday='{self.birthday}', phone_number='{self.phone_number}', "
                f"driver_license='{self.driver_license}', vehicle_title='{self.vehicle_title}', "
                f"insurance_policy='{self.insurance_policy}', license_plate='{self.license_plate}', "
                f"experience={self.experience})")

class DriverShort:
    """Короткая версия класса Driver с валидацией."""
    def __init__(self, last_name, first_name, patronymic, experience):
        self.last_name = Validator.validate_string(last_name, "Фамилия")
        self.first_name = Validator.validate_string(first_name, "Имя")
        self.patronymic = Validator.validate_string(patronymic, "Отчество")
        self.experience = Validator.validate_positive_integer(experience, "Стаж")

    def __repr__(self):
        return (f"DriverShort(last_name={self.last_name}, first_name={self.first_name}, "
                f"patronymic={self.patronymic}, experience={self.experience})")

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}, Стаж: {self.experience} лет"


class DriversRepositoryJSON(MyEntityRepository):
    """Репозиторий для работы с водителями в формате JSON."""

    def load_entities(self):
        """Загрузка данных из JSON-файла."""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Driver(**entry) for entry in data]
        except FileNotFoundError:
            return []

    def save_entities(self):
        """Сохранение данных в JSON-файл."""
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([entity.__dict__ for entity in self.entities], file, ensure_ascii=False, indent=4)

class DriversRepositoryYAML(MyEntityRepository):
    """Репозиторий для работы с водителями в формате YAML."""

    def load_entities(self):
        """Загрузка данных из YAML-файла."""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file)
                return [Driver(**entry) for entry in data]
        except FileNotFoundError:
            return []

    def save_entities(self):
        """Сохранение данных в YAML-файл."""
        with open(self.filename, "w", encoding="utf-8") as file:
            yaml.dump([entity.__dict__ for entity in self.entities], file, allow_unicode=True)


class DriversRepositoryDB(MyEntityRepository):
    """Репозиторий для работы с таблицей drivers в базе данных."""

    def __init__(self, db_name):
        self.db_manager = DBConnectionManager(db_name)
        self._initialize_table()

    def _initialize_table(self):
        """Создание таблицы, если её нет."""
        query = """
        CREATE TABLE IF NOT EXISTS drivers (
            DriverId INTEGER PRIMARY KEY AUTOINCREMENT,
            LastName TEXT NOT NULL,
            FirstName TEXT NOT NULL,
            Patronymic TEXT NOT NULL,
            Birthday TEXT NOT NULL,
            PhoneNumber TEXT NOT NULL,
            DriverLicense TEXT NOT NULL,
            VehicleTitle TEXT NOT NULL,
            InsurancePolicy TEXT NOT NULL,
            LicensePlate TEXT NOT NULL,
            Experience INTEGER NOT NULL
        )
        """
        self.db_manager.execute_query(query)
        self.db_manager.commit()

    def get_by_id(self, driver_id):
        """Получить водителя по ID."""
        query = "SELECT * FROM drivers WHERE DriverId = ?"
        cursor = self.db_manager.execute_query(query, (driver_id,))
        result = cursor.fetchone()
        if result:
            return Driver(**result)
        return None

    def get_k_n_short_list(self, k, n):
        """Получить список k по счету n объектов класса Driver."""
        offset = (k - 1) * n
        query = """
            SELECT DriverId, LastName, FirstName, Patronymic, Birthday, PhoneNumber, DriverLicense,
                   VehicleTitle, InsurancePolicy, LicensePlate, Experience
            FROM drivers
            LIMIT ? OFFSET ?
        """
        cursor = self.db_manager.execute_query(query, (n, offset))
        results = cursor.fetchall()
        return [Driver(**dict(row)) for row in results]

    def add_entity(self, driver):
        """Добавить водителя в базу данных."""
        query = """INSERT INTO drivers (LastName, FirstName, Patronymic, Birthday, PhoneNumber, 
                   DriverLicense, VehicleTitle, InsurancePolicy, LicensePlate, Experience) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        self.db_manager.execute_query(query, (
            driver.last_name, driver.first_name, driver.patronymic, driver.birthday,
            driver.phone_number, driver.driver_license, driver.vehicle_title,
            driver.insurance_policy, driver.license_plate, driver.experience
        ))
        self.db_manager.commit()

    def replace_entity_by_id(self, driver_id, updated_driver):
        """Обновить водителя по ID."""
        query = """UPDATE drivers SET LastName = ?, FirstName = ?, Patronymic = ?, Birthday = ?, 
                   PhoneNumber = ?, DriverLicense = ?, VehicleTitle = ?, InsurancePolicy = ?, 
                   LicensePlate = ?, Experience = ? WHERE DriverId = ?"""
        self.db_manager.execute_query(query, (
            updated_driver.last_name, updated_driver.first_name, updated_driver.patronymic,
            updated_driver.birthday, updated_driver.phone_number, updated_driver.driver_license,
            updated_driver.vehicle_title, updated_driver.insurance_policy,
            updated_driver.license_plate, updated_driver.experience, driver_id
        ))
        self.db_manager.commit()

    def delete_entity_by_id(self, driver_id):
        """Удалить водителя по ID."""
        query = "DELETE FROM drivers WHERE DriverId = ?"
        self.db_manager.execute_query(query, (driver_id,))
        self.db_manager.commit()

    def get_count(self):
        """Получить количество водителей."""
        query = "SELECT COUNT(*) FROM drivers"
        cursor = self.db_manager.execute_query(query)
        result = cursor.fetchone()
        return result[0] if result else 0