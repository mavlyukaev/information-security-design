from model import Model
from iview import IView
from urllib.parse import parse_qs

class Controller:
    def __init__(self, model: Model, view: IView):
        self.model = model
        self.view = view

    def index(self):
        """Главная страница с таблицей записей"""
        records = self.model.get_all_records()
        rows = "\n".join(
            f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td>"
            f"<td><a href='/details/{r[0]}'>Детали</a> | <a href='/edit/{r[0]}'>Редактировать</a> | <a href='/delete/{r[0]}'>Удалить</a></td></tr>"
            for r in records
        )
        return self.view.render_template("index.html", records=rows)

    def details(self, record_id):
        """Просмотр деталей записи"""
        record = self.model.get_record_by_id(record_id)
        if record:
            record_dict = {
                "id": record[0],
                "last_name": record[1],
                "first_name": record[2],
                "patronymic": record[3],
                "experience": record[4],
            }
            return self.view.render_template("details.html", **record_dict)
        return self.view.render_template("error.html", message="Запись не найдена")

    def add_form(self):
        """Отобразить форму добавления записи"""
        return self.view.render_template("add.html")

    def add_record(self, post_data):
        """Добавить новую запись"""
        data = parse_qs(post_data)
        last_name = data["last_name"][0]
        first_name = data["first_name"][0]
        patronymic = data.get("patronymic", [""])[0]  # Отчество может быть пустым
        experience = int(data["experience"][0])

        # Проверка стажа на валидность
        if experience < 0:
            return self.view.render_template("error.html", message="Ошибка: Стаж не может быть отрицательным.")

        # Добавление записи
        self.model.add_record(last_name, first_name, patronymic, experience)
        return self.view.render_template("success.html", message="Запись успешно добавлена!")

    def edit_form(self, record_id):
        """Отобразить форму редактирования записи"""
        record = self.model.get_record_by_id(record_id)
        if record:
            record_dict = {
                "id": record[0],
                "last_name": record[1],
                "first_name": record[2],
                "patronymic": record[3],
                "experience": record[4],
            }
            return self.view.render_template("edit.html", **record_dict)
        return self.view.render_template("error.html", message="Запись не найдена")

    def update_record(self, record_id, post_data):
        """Обновить существующую запись"""
        data = parse_qs(post_data)
        last_name = data["last_name"][0]
        first_name = data["first_name"][0]
        patronymic = data.get("patronymic", [""])[0]
        experience = int(data["experience"][0])

        # Проверка стажа на валидность
        if experience < 0:
            return self.view.render_template("error.html", message="Ошибка: Стаж не может быть отрицательным.")

        # Обновление записи
        self.model.update_record(record_id, last_name, first_name, patronymic, experience)
        return self.view.render_template("success.html", message="Запись успешно обновлена!")

    def delete_record(self, record_id):
        """Удалить запись"""
        self.model.delete_record(record_id)
        return self.view.render_template("success.html", message="Запись успешно удалена!")
