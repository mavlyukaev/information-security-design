import os
import sqlite3
import re
from datetime import datetime
import json
import yaml


class Validator:
    """Общие методы для проверки данных."""

    @staticmethod
    def validate_positive_integer(value, field_name):
        """Проверка, что значение является положительным целым числом."""
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{field_name} должен быть положительным целым числом.")
        return value

    @staticmethod
    def validate_string(value, field_name):
        """Проверка, что строка не пустая."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} не может быть пустым.")
        return value.strip()

    @staticmethod
    def validate_date(value, field_name):
        """Проверка и форматирование даты (ДД.ММ.ГГГГ)."""
        try:
            date_obj = datetime.strptime(value, "%d.%m.%Y")
            return date_obj.strftime("%d.%m.%Y")
        except ValueError:
            raise ValueError(f"{field_name} имеет неверный формат даты. Ожидается ДД.ММ.ГГГГ.")

    @staticmethod
    def validate_phone_number(value, field_name):
        """Проверка номера телефона с маской +7(XXX)XXX-XX-XX."""
        phone_pattern = r"^\+7\(\d{3}\)\d{3}-\d{2}-\d{2}$"
        if not re.match(phone_pattern, value):
            raise ValueError(f"{field_name} должен быть в формате +7(XXX)XXX-XX-XX.")
        return value

    @staticmethod
    def validate_license(value, field_name):
        """Проверка лицензий и идентификаторов с форматом 'NN NN NNNNNN'."""
        license_pattern = r"^\d{2} \d{2} \d{6}$"
        if not re.match(license_pattern, value):
            raise ValueError(f"{field_name} должен быть в формате 'NN NN NNNNNN'.")
        return value

    @staticmethod
    def validate_policy(value, field_name):
        """Проверка страхового полиса с форматом 'NNN NNNNNNNNNNN'."""
        policy_pattern = r"^\d{3} \d{12}$"
        if not re.match(policy_pattern, value):
            raise ValueError(f"{field_name} должен быть в формате 'NNN NNNNNNNNNNN'.")
        return value

    @staticmethod
    def validate_license_plate(value, field_name):
        """Проверка номерного знака машины."""
        license_plate_pattern = r"^[А-Яа-я]\d{3}[А-Яа-я]{2}\d{2,3}$"
        if not re.match(license_plate_pattern, value):
            raise ValueError(f"{field_name} должен быть в формате 'А111АА111'.")
        return value

    @staticmethod
    def validate_bonus(value, field_name):
        """Проверка бонуса (премии), должен быть числом 0 или больше."""
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(f"{field_name} должен быть числом 0 или больше.")
        return value
    
    @staticmethod
    def validate_departure_and_arrival_dates(departure_date, arrival_date):
        """Проверка, что дата отправки не позже даты прибытия."""
        try:
            dep_date = datetime.strptime(departure_date, "%d.%m.%Y")
            arr_date = datetime.strptime(arrival_date, "%d.%m.%Y")
            if dep_date > arr_date:
                raise ValueError("Дата отправки не может быть позже даты прибытия.")
        except ValueError as e:
            raise ValueError(f"Ошибка проверки дат: {e}")
        return departure_date, arrival_date


class MyEntityRepository:
    """Базовый класс репозитория."""
    def __init__(self, filename):
        self.filename = filename
        self.entities = self.load_entities()

    def load_entities(self):
        """Загрузить данные из файла. Реализовать в дочерних классах."""
        raise NotImplementedError("Метод load_entities должен быть реализован в дочернем классе.")

    def save_entities(self):
        """Сохранить данные в файл. Реализовать в дочерних классах."""
        raise NotImplementedError("Метод save_entities должен быть реализован в дочернем классе.")

    def get_by_id(self, entity_id):
        """Получить объект по ID."""
        for entity in self.entities:
            if entity.get_id() == entity_id:
                return entity
        return None

    def get_k_n_short_list(self, k, n):
        """Получить список k по счету n объектов."""
        start_index = (k - 1) * n
        end_index = start_index + n
        return self.entities[start_index:end_index]

    def sort_by_field(self, field):
        """Сортировать элементы по выбранному полю."""
        if hasattr(self.entities[0], field):
            self.entities.sort(key=lambda x: getattr(x, field))
        else:
            raise ValueError(f"Поле {field} не существует в классе {type(self.entities[0]).__name__}.")

    def add_entity(self, entity):
        """Добавить объект в список с новым ID."""
        new_id = max([e.get_id() for e in self.entities], default=0) + 1
        entity.set_id(new_id)
        self.entities.append(entity)
        self.save_entities()

    def replace_entity_by_id(self, entity_id, updated_entity):
        """Заменить элемент списка по ID."""
        for index, entity in enumerate(self.entities):
            if entity.get_id() == entity_id:
                updated_entity.set_id(entity_id)
                self.entities[index] = updated_entity
                self.save_entities()
                return
        raise ValueError(f"Объект с ID {entity_id} не найден.")

    def delete_entity_by_id(self, entity_id):
        """Удалить элемент списка по ID."""
        self.entities = [entity for entity in self.entities if entity.get_id() != entity_id]
        self.save_entities()

    def get_count(self):
        """Получить количество элементов."""
        return len(self.entities)


class DBConnectionManager:
    """Менеджер соединений с базой данных (Singleton)."""
    _instances = {}

    def __new__(cls, db_name="database.db"):
        if db_name not in cls._instances:
            cls._instances[db_name] = super(DBConnectionManager, cls).__new__(cls)
            cls._instances[db_name]._init_connection(db_name)
        return cls._instances[db_name]

    def _init_connection(self, db_name):
        """Инициализация соединения с базой данных SQLite."""
        if not os.path.exists(os.path.dirname(db_name)):
            os.makedirs(os.path.dirname(db_name), exist_ok=True)
        self.connection = sqlite3.connect(db_name)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def execute_query(self, query, params=None):
        """Выполнить SQL-запрос."""
        if params is None:
            params = ()
        self.cursor.execute(query, params)
        return self.cursor

    def commit(self):
        """Подтвердить транзакцию."""
        self.connection.commit()

    def close(self):
        """Закрыть соединение с базой данных."""
        self.connection.close()

    def __del__(self):
        """Закрыть соединение при удалении объекта."""
        self.close()