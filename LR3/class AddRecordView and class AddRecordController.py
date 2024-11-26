class AddRecordView:
    def __init__(self):
        self.submit_callback = None
        self.cancel_callback = None

    def show(self):
        """Отобразить окно для добавления записи"""
        print("Окно добавления записи открыто.")

    def set_submit_callback(self, callback):
        """Установить обработчик для кнопки 'Добавить'"""
        self.submit_callback = callback

    def set_cancel_callback(self, callback):
        """Установить обработчик для кнопки 'Отмена'"""
        self.cancel_callback = callback

    def get_input_data(self):
        """Получить данные от пользователя (эмулируем)"""
        return {
            "LastName": input("Введите фамилию: "),
            "FirstName": input("Введите имя: "),
            "Patronymic": input("Введите отчество: "),
            "Experience": input("Введите опыт (число): "),
        }

    def close(self):
        """Закрыть окно"""
        print("Окно добавления записи закрыто.")

class AddRecordController:
    def __init__(self, repository, add_record_view, main_controller):
        self.repository = repository
        self.add_record_view = add_record_view
        self.main_controller = main_controller

        # Устанавливаем обработчики событий представления
        self.add_record_view.set_submit_callback(self.add_record)
        self.add_record_view.set_cancel_callback(self.cancel)

    def start(self):
        """Запуск окна добавления записи"""
        self.add_record_view.show()

    def add_record(self):
        """Добавить запись в репозиторий"""
        # Получаем данные от пользователя
        data = self.add_record_view.get_input_data()

        # Валидация данных
        if not self.validate_data(data):
            print("Ошибка валидации данных!")
            return

        # Добавление в репозиторий
        self.repository.add_entity(data)

        # Уведомление главного окна
        self.main_controller.on_repository_updated(self.repository.load_entities())

        # Закрыть окно
        self.add_record_view.close()

    def cancel(self):
        """Закрыть окно без добавления записи"""
        self.add_record_view.close()

    def validate_data(self, data):
        """Проверка данных"""
        try:
            if not data["LastName"] or not data["FirstName"]:
                return False
            if not data["Experience"].isdigit() or int(data["Experience"]) < 0:
                return False
            return True
        except KeyError:
            return False

from view import MainView, AddRecordView
from controller import MainController, AddRecordController
from repository import RepositoryWithObserver

if __name__ == "__main__":
    # Создание репозитория и главного окна
    repository = RepositoryWithObserver()
    main_view = MainView()
    main_controller = MainController(repository, main_view)

    # Открытие главного окна
    main_controller.start()

    # Добавление записи через новое окно
    add_record_view = AddRecordView()
    add_record_controller = AddRecordController(repository, add_record_view, main_controller)
    add_record_controller.start()
