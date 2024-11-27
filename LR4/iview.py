from abc import ABC, abstractmethod

class IView(ABC):
    @abstractmethod
    def display_records(self, records):
        """Отобразить список записей"""
        pass

    @abstractmethod
    def display_details(self, record):
        """Отобразить подробности записи"""
        pass

    @abstractmethod
    def get_user_input(self):
        """Получить ввод пользователя"""
        pass

    @abstractmethod
    def display_message(self, message):
        """Вывести сообщение пользователю"""
        pass
