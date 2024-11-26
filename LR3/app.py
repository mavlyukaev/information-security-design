import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class DBConnectionManager:
    def __init__(self, db_name="drivers.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._initialize_table()

    def _initialize_table(self):
        """Создание таблицы drivers, если её нет"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS drivers (
                DriverId INTEGER PRIMARY KEY AUTOINCREMENT,
                LastName TEXT NOT NULL,
                FirstName TEXT NOT NULL,
                Patronymic TEXT,
                Experience INTEGER NOT NULL
            )
        """)
        self.connection.commit()

    def execute_query(self, query, params=None):
        """Выполняет SQL-запрос с параметрами"""
        if params is None:
            params = ()
        self.cursor.execute(query, params)
        return self.cursor

    def commit(self):
        """Подтверждает транзакцию"""
        self.connection.commit()

    def __del__(self):
        """Закрывает соединение с БД"""
        self.cursor.close()
        self.connection.close()


class RepositoryWithObserver:
    def __init__(self, db_name="drivers.db"):
        self.db_manager = DBConnectionManager(db_name)
        self.observers = []

    def add_observer(self, observer):
        """Добавить наблюдателя"""
        self.observers.append(observer)

    def notify_observers(self):
        """Уведомить наблюдателей об изменениях"""
        data = self.get_all_records()
        for observer in self.observers:
            observer.update(data)

    def add_record(self, record):
        """Добавить запись в базу данных"""
        query = "INSERT INTO drivers (LastName, FirstName, Patronymic, Experience) VALUES (?, ?, ?, ?)"
        self.db_manager.execute_query(query, (record['LastName'], record['FirstName'], record['Patronymic'], record['Experience']))
        self.db_manager.commit()
        self.notify_observers()

    def delete_record(self, record_id):
        """Удалить запись по ID"""
        query = "DELETE FROM drivers WHERE DriverId = ?"
        self.db_manager.execute_query(query, (record_id,))
        self.db_manager.commit()
        self.notify_observers()

    def sort_by_field(self, field):
        """Сортировать записи по указанному полю"""
        query = f"SELECT DriverId, LastName, FirstName, Experience FROM drivers ORDER BY {field}"
        cursor = self.db_manager.execute_query(query)
        return cursor.fetchall()

    def get_all_records(self):
        """Получить все записи"""
        query = "SELECT DriverId, LastName, FirstName, Experience FROM drivers"
        cursor = self.db_manager.execute_query(query)
        return cursor.fetchall()

    def get_by_id(self, driver_id):
        """Получить запись по ID"""
        query = "SELECT * FROM drivers WHERE DriverId = ?"
        cursor = self.db_manager.execute_query(query, (driver_id,))
        return cursor.fetchone()



class MainView:
    """Представление: основное окно"""
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Управление водителями")

        # Таблица для отображения данных
        self.table = ttk.Treeview(self.root, columns=("ID", "LastName", "FirstName", "Experience"), show="headings")
        self.table.heading("ID", text="ID", command=lambda: self.sort_table("DriverId"))
        self.table.heading("LastName", text="Фамилия", command=lambda: self.sort_table("LastName"))
        self.table.heading("FirstName", text="Имя", command=lambda: self.sort_table("FirstName"))
        self.table.heading("Experience", text="Опыт (лет)", command=lambda: self.sort_table("Experience"))
        self.table.pack(fill=tk.BOTH, expand=True)

        # Кнопки управления
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill=tk.X)

        tk.Button(btn_frame, text="Добавить", command=self.open_add_record_window).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(btn_frame, text="Удалить", command=self.delete_record).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(btn_frame, text="Детали", command=self.open_details_window).pack(side=tk.LEFT, padx=5, pady=5)

    def sort_table(self, field):
        """Обработать сортировку по полю"""
        self.controller.sort_records(field)

    def open_add_record_window(self):
        """Открыть окно добавления записи"""
        self.controller.open_add_record_window()

    def delete_record(self):
        """Удалить выбранную запись"""
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите запись для удаления")
            return
        driver_id = self.table.item(selected_item, "values")[0]
        self.controller.delete_record(driver_id)

    def open_details_window(self):
        """Открыть окно с полными деталями"""
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите запись для просмотра")
            return
        driver_id = self.table.item(selected_item, "values")[0]
        self.controller.open_details_window(driver_id)

    def update_table(self, data):
        """Обновить таблицу с данными"""
        for item in self.table.get_children():
            self.table.delete(item)
        for row in data:
            self.table.insert("", tk.END, values=row)



class MainController:
    """Контроллер"""
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.model.add_observer(self)

    def update(self, data):
        """Обновить представление"""
        self.view.update_table(data)

    def open_add_record_window(self):
        """Открыть окно добавления записи"""
        AddRecordWindow(self.model)

    def delete_record(self, driver_id):
        """Удалить запись"""
        self.model.delete_record(driver_id)

    def open_details_window(self, driver_id):
        """Открыть окно деталей"""
        details = self.model.get_by_id(driver_id)
        if details:
            messagebox.showinfo("Детали", f"ID: {details[0]}\nФамилия: {details[1]}\nИмя: {details[2]}\n"
                                          f"Отчество: {details[3]}\nОпыт: {details[4]} лет")

    def sort_records(self, field):
        """Сортировать записи"""
        sorted_data = self.model.sort_by_field(field)
        self.view.update_table(sorted_data)


class AddRecordWindow:
    """Окно добавления записи"""
    def __init__(self, model):
        self.model = model
        self.window = tk.Toplevel()
        self.window.title("Добавить запись")

        tk.Label(self.window, text="Фамилия").grid(row=0, column=0)
        tk.Label(self.window, text="Имя").grid(row=1, column=0)
        tk.Label(self.window, text="Отчество").grid(row=2, column=0)
        tk.Label(self.window, text="Опыт (лет)").grid(row=3, column=0)

        self.last_name_entry = tk.Entry(self.window)
        self.first_name_entry = tk.Entry(self.window)
        self.patronymic_entry = tk.Entry(self.window)
        self.experience_entry = tk.Entry(self.window)

        self.last_name_entry.grid(row=0, column=1)
        self.first_name_entry.grid(row=1, column=1)
        self.patronymic_entry.grid(row=2, column=1)
        self.experience_entry.grid(row=3, column=1)

        tk.Button(self.window, text="Добавить", command=self.add_record).grid(row=4, column=0, columnspan=2)

    def add_record(self):
        """Добавить запись в базу данных"""
        record = {
            "LastName": self.last_name_entry.get(),
            "FirstName": self.first_name_entry.get(),
            "Patronymic": self.patronymic_entry.get(),
            "Experience": int(self.experience_entry.get())
        }
        self.model.add_record(record)
        self.window.destroy()


if __name__ == "__main__":
    # Инициализация компонентов
    model = RepositoryWithObserver()
    view = MainView(None)
    controller = MainController(model, view)
    view.controller = controller

    # Запуск приложения
    view.root.mainloop()
