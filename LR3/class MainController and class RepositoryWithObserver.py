class MainController:
    def __init__(self, repository, main_view):
        self.repository = repository
        self.main_view = main_view

        # Подписываемся на обновления репозитория
        self.repository.add_observer(self)

        # Устанавливаем обработчики событий представления
        self.main_view.set_open_details_callback(self.open_details_window)

    def start(self):
        """Запуск главного окна приложения"""
        data = self.repository.load_entities()
        self.main_view.show(data)

    def on_repository_updated(self, updated_data):
        """Обработка уведомлений от репозитория"""
        self.main_view.update_table(updated_data)

    def open_details_window(self, item_id):
        """Открыть окно с полной информацией"""
        full_data = self.repository.get_by_id(item_id)
        self.main_view.open_details(full_data)

class RepositoryWithObserver:
    def __init__(self):
        self.data = []
        self.observers = []

    def add_observer(self, observer):
        """Добавить наблюдателя"""
        self.observers.append(observer)

    def notify_observers(self):
        """Уведомить всех наблюдателей об обновлении данных"""
        for observer in self.observers:
            observer.on_repository_updated(self.data)

    def load_entities(self):
        """Загрузка данных (например, из базы данных)"""
        self.data = self.fetch_data_from_db()
        self.notify_observers()
        return self.data
