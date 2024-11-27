from http.server import BaseHTTPRequestHandler, HTTPServer
from controller import Controller
from model import Model
from view import View
from urllib.parse import parse_qs, unquote


class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        model = Model()
        view = View()
        self.controller = Controller(model, view)
        super().__init__(*args, **kwargs)

    def do_GET(self):
        try:
            if self.path == "/":
                self._send_response(200, self.controller.index())
            elif self.path.startswith("/details/"):
                record_id = self._extract_record_id()
                if record_id is not None:
                    self._send_response(200, self.controller.details(record_id))
                else:
                    self._send_response(400, "<h1>Ошибка</h1><p>Некорректный ID записи.</p>")
            elif self.path == "/add":
                self._send_response(200, self.controller.add_form())
            elif self.path.startswith("/edit/"):
                record_id = self._extract_record_id()
                if record_id is not None:
                    self._send_response(200, self.controller.edit_form(record_id))
                else:
                    self._send_response(400, "<h1>Ошибка</h1><p>Некорректный ID записи.</p>")
            elif self.path.startswith("/delete/"):
                record_id = self._extract_record_id()
                if record_id is not None:
                    self.controller.delete_record(record_id)
                    self._redirect("/")
                else:
                    self._send_response(400, "<h1>Ошибка</h1><p>Некорректный ID записи.</p>")
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
                if "Ошибка" in response:
                    self._send_response(400, f"<h1>Ошибка добавления</h1><p>{response}</p>")
                else:
                    self._redirect("/")
            elif self.path.startswith("/edit/"):
                record_id = self._extract_record_id()
                if record_id is not None:
                    response = self.controller.update_record(record_id, post_data)
                    if "Ошибка" in response:
                        self._send_response(400, f"<h1>Ошибка редактирования</h1><p>{response}</p>")
                    else:
                        self._redirect("/")
                else:
                    self._send_response(400, "<h1>Ошибка</h1><p>Некорректный ID записи.</p>")
            else:
                self._send_response(404, "<h1>404</h1><p>Маршрут не найден.</p>")
        except ValueError as e:
            self._send_response(400, f"<h1>Ошибка</h1><p>Некорректный ввод данных: {e}</p>")
        except Exception as e:
            self._send_response(500, f"<h1>Ошибка сервера</h1><p>{e}</p>")

    def _send_response(self, status, content, content_type="text/html"):
        self.send_response(status)
        self.send_header("Content-type", content_type)
        self.end_headers()
        if isinstance(content, str):
            self.wfile.write(content.encode())
        elif isinstance(content, bytes):
            self.wfile.write(content)

    def _redirect(self, location):
        self.send_response(302)
        self.send_header("Location", location)
        self.end_headers()

    def _extract_record_id(self):
        try:
            record_id = int(unquote(self.path.split("/")[-1]))
            return record_id
        except ValueError:
            return None


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8080), RequestHandler)
    print("Сервер запущен на http://localhost:8080")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
        server.server_close()
