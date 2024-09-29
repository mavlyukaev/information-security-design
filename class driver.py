class Driver:
    def __init__(self, driver_id: int, last_name: str, first_name: str, patronymic: str, experience: int):
        self.__driver_id = driver_id
        self.__last_name = last_name
        self.__first_name = first_name
        self.__patronymic = patronymic
        self.__experience = experience

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

    # Setters
    def set_driver_id(self, driver_id: int):
        self.__driver_id = driver_id

    def set_last_name(self, last_name: str):
        self.__last_name = last_name

    def set_first_name(self, first_name: str):
        self.__first_name = first_name

    def set_patronymic(self, patronymic: str):
        self.__patronymic = patronymic

    def set_experience(self, experience: int):
        if experience >= 0:
            self.__experience = experience
        else:
            raise ValueError("Опыт не может быть меньше 0")

    # Cтроковое представление информации о водителе
    def __str__(self):
        return (f"Driver ID: {self.__driver_id}, Name: {self.__last_name} {self.__first_name} {self.__patronymic}, "
                f"Experience: {self.__experience} years")