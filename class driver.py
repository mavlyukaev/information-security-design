import json


class Driver:
    def __init__(self, driver_id=None, last_name=None, first_name=None, patronymic=None, experience=None):
        if isinstance(driver_id, str):
            # Инициализация из строки
            self.initialize_from_string(driver_id)
        elif isinstance(driver_id, dict):
            # Инициализация из JSON (словарь)
            self.initialize_from_json(driver_id)
        else:
            # Инициализация из отдельных параметров
            self.set_driver_id(driver_id)
            self.set_last_name(last_name)
            self.set_first_name(first_name)
            self.set_patronymic(patronymic)
            self.set_experience(experience)

    # Инициализация из строки
    def initialize_from_string(self, data_str: str):
        data = data_str.split(',')
        if len(data) != 5:
            raise ValueError(
                "String must contain exactly 5 values: driver_id,last_name,first_name,patronymic,experience")

        driver_id, last_name, first_name, patronymic, experience = data
        self.set_driver_id(int(driver_id))
        self.set_last_name(last_name.strip())
        self.set_first_name(first_name.strip())
        self.set_patronymic(patronymic.strip())
        self.set_experience(int(experience))

    # Инициализация из JSON (словаря)
    def initialize_from_json(self, json_data: dict):
        self.set_driver_id(json_data.get('driver_id'))
        self.set_last_name(json_data.get('last_name'))
        self.set_first_name(json_data.get('first_name'))
        self.set_patronymic(json_data.get('patronymic'))
        self.set_experience(json_data.get('experience'))

    # Статические методы для валидации
    @staticmethod
    def validate_string(value: str, field_name: str) -> bool:
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError(f"{field_name} must be a non-empty string")
        return True

    @staticmethod
    def validate_driver_id(driver_id: int) -> bool:
        if not isinstance(driver_id, int) or driver_id <= 0:
            raise ValueError("Driver ID must be a positive integer")
        return True

    @staticmethod
    def validate_experience(experience: int) -> bool:
        if not isinstance(experience, int) or experience < 0:
            raise ValueError("Experience must be a non-negative integer")
        return True

    # Getters
    def get_driver_id(self):
        return self.__driver_id

    def get_last_name(self):
        return self.__last_name

    def get_first_name(self):
        return self.__first_name

    def get_patronymic(self):
        return self.__patronymic

    def get_experience(self):
        return self.__experience

    # Setters с валидацией
    def set_driver_id(self, driver_id: int):
        self.validate_driver_id(driver_id)
        self.__driver_id = driver_id

    def set_last_name(self, last_name: str):
        self.validate_string(last_name, "Last name")
        self.__last_name = last_name

    def set_first_name(self, first_name: str):
        self.validate_string(first_name, "First name")
        self.__first_name = first_name

    def set_patronymic(self, patronymic: str):
        self.validate_string(patronymic, "Patronymic")
        self.__patronymic = patronymic

    def set_experience(self, experience: int):
        self.validate_experience(experience)
        self.__experience = experience

    # Cтроковое представление информации о водителе
    def __str__(self):
        return (f"Driver ID: {self.__driver_id}, Name: {self.__last_name} {self.__first_name} {self.__patronymic}, "
                f"Experience: {self.__experience} years")