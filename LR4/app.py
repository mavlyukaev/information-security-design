from http.server import BaseHTTPRequestHandler, HTTPServer
from controller import Controller
from view import WebView
from model import Model


class WebRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.controller = Controller(Model(), WebView())  # Передаем модель и представление
        super().__init__(*args, **kwargs)

    def do_GET(self):
        try:
            if self.path == "/":
                response = self.controller.index()
                self._send_response(200, response)
            elif self.path.startswith("/details/"):
                record_id = int(self.path.split("/")[-1])
                response = self.controller.details(record_id)
                self._send_response(200, response)
            elif self.path == "/add":
                response = self.controller.add_form()
                self._send_response(200, response)
            elif self.path.startswith("/edit/"):
                record_id = int(self.path.split("/")[-1])
                response = self.controller.edit_form(record_id)
                self._send_response(200, response)
            elif self.path.startswith("/delete/"):  # Добавляем обработку DELETE-запроса
                record_id = int(self.path.split("/")[-1])
                self.controller.delete_record(record_id)
                self._redirect("/")  # Перенаправляем пользователя на главную страницу
            else:
                self._send_response(404, "<h1>404</h1><p>Страница не найдена.</p>")
        except Exception as e:
            self._send_response(500, f"<h1>Ошибка сервера</h1><p>{e}</p>")

    def do_POST(self):
        try:
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length).decode()

            if self.path == "/add":
                response = self.controller.add_record(post_data)
                self._send_response(200, response)
            elif self.path.startswith("/edit/"):
                record_id = int(self.path.split("/")[-1])
                response = self.controller.update_record(record_id, post_data)
                self._send_response(200, response)
        except Exception as e:
            self._send_response(500, f"<h1>Ошибка сервера</h1><p>{e}</p>")

    def _send_response(self, status, content):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode())

    def _redirect(self, location):
        """Перенаправление пользователя на другой маршрут"""
        self.send_response(302)
        self.send_header("Location", location)
        self.end_headers()


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8080), WebRequestHandler)
    print("Сервер запущен на http://localhost:8080")
    server.serve_forever()
