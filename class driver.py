class Driver:
    def __init__(self, driver_id: int, last_name: str, first_name: str, patronymic: str, experience: int):
        # Проверка всех полей с помощью статических методов
        if self.validate_driver_id(driver_id) and \
                self.validate_name(last_name) and \
                self.validate_name(first_name) and \
                self.validate_name(patronymic) and \
                self.validate_experience(experience):
            self.__driver_id = driver_id
            self.__last_name = last_name
            self.__first_name = first_name
            self.__patronymic = patronymic
            self.__experience = experience
        else:
            raise ValueError("Invalid field values provided")

    # Статический метод для проверки идентификатора водителя
    @staticmethod
    def validate_driver_id(driver_id: int) -> bool:
        return isinstance(driver_id, int) and driver_id > 0

    # Статический метод для проверки имени, фамилии, отчества
    @staticmethod
    def validate_name(name: str) -> bool:
        return isinstance(name, str) and len(name.strip()) > 0

    # Статический метод для проверки опыта водителя
    @staticmethod
    def validate_experience(experience: int) -> bool:
        return isinstance(experience, int) and experience >= 0

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
        if self.validate_driver_id(driver_id):
            self.__driver_id = driver_id
        else:
            raise ValueError("Invalid Driver ID")

    def set_last_name(self, last_name: str):
        if self.validate_name(last_name):
            self.__last_name = last_name
        else:
            raise ValueError("Invalid last name")

    def set_first_name(self, first_name: str):
        if self.validate_name(first_name):
            self.__first_name = first_name
        else:
            raise ValueError("Invalid first name")

    def set_patronymic(self, patronymic: str):
        if self.validate_name(patronymic):
            self.__patronymic = patronymic
        else:
            raise ValueError("Invalid patronymic")

    def set_experience(self, experience: int):
        if self.validate_experience(experience):
            self.__experience = experience
        else:
            raise ValueError("Invalid experience value")

    # Cтроковое представление информации о водителе
    def __str__(self):
        return (f"Driver ID: {self.__driver_id}, Name: {self.__last_name} {self.__first_name} {self.__patronymic}, "
                f"Experience: {self.__experience} years")