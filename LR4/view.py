import os
from iview import IView

class View(IView):
    def display_records(self, records):
        """Отображение списка записей в консоли"""
        print("\nСписок записей:")
        for record in records:
            print(f"ID: {record['id']}, Имя: {record['name']}, Опыт: {record['experience']} лет")

    def display_details(self, record):
        """Отображение подробностей записи в консоли"""
        print("\nДетали записи:")
        for key, value in record.items():
            print(f"{key.capitalize()}: {value}")

    def get_user_input(self):
        """Получить ввод пользователя для выбора действия"""
        print("\nВыберите действие:")
        print("1. Добавить запись")
        print("2. Удалить запись")
        print("3. Редактировать запись")
        print("4. Просмотреть запись")
        print("5. Выход")
        return input("Введите номер действия: ")

    def display_message(self, message):
        """Вывод сообщения для пользователя"""
        print(f"\n{message}")

    @staticmethod
    def render_template(template_name, **kwargs):
        """Рендеринг HTML-шаблона с заменой переменных"""
        base_path = os.path.dirname(__file__)
        template_path = os.path.join(base_path, "templates", template_name)
        
        # Проверяем наличие шаблона
        if not os.path.exists(template_path):
            return f"Ошибка: Шаблон {template_name} не найден."
        
        with open(template_path, "r", encoding="utf-8") as file:
            html = file.read()
            # Заменяем переменные в шаблоне
            for key, value in kwargs.items():
                html = html.replace(f"{{{{ {key} }}}}", str(value))
        return html
