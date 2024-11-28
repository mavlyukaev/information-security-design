from iview import IView 
import os

class WebView(IView):
    def display_records(self, records):
        """Рендеринг списка записей в веб-шаблоне"""
        rows = "\n".join(
            f"<tr><td>{record['id']}</td><td>{record['name']}</td><td>{record['experience']}</td>"
            f"<td><a href='/details/{record['id']}'>Детали</a> | "
            f"<a href='/edit/{record['id']}'>Редактировать</a> | "
            f"<a href='/delete/{record['id']}'>Удалить</a></td></tr>"
            for record in records
        )
        return self.render_template("index.html", rows=rows)

    def display_details(self, record):
        """Рендеринг деталей записи в веб-шаблоне"""
        return self.render_template("details.html", **record)

    def display_message(self, message):
        """Рендеринг сообщения"""
        return self.render_template("success.html", message=message)

    @staticmethod
    def render_template(template_name, **kwargs):
        """Рендеринг HTML-шаблона с заменой переменных"""
        base_path = os.path.dirname(__file__)
        template_path = os.path.join(base_path, "templates", template_name)
        
        if not os.path.exists(template_path):
            return f"Ошибка: Шаблон {template_name} не найден."
        
        with open(template_path, "r", encoding="utf-8") as file:
            html = file.read()
            for key, value in kwargs.items():
                html = html.replace(f"{{{{ {key} }}}}", str(value))
        return html

    def get_user_input(self):
        """Заглушка метода для веб-приложения."""
        return None
