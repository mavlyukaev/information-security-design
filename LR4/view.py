import os

class View:
    @staticmethod
    def render_template(template_name, **kwargs):
        # Определяем абсолютный путь к файлу шаблона
        base_path = os.path.dirname(__file__)
        template_path = os.path.join(base_path, "templates", template_name)
        
        # Открываем файл шаблона
        with open(template_path, "r", encoding="utf-8") as file:
            html = file.read()
            # Заменяем переменные в шаблоне
            for key, value in kwargs.items():
                html = html.replace(f"{{{{ {key} }}}}", str(value))
        return html
