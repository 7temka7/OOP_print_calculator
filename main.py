from pathlib import Path
import flet as ft
from models import Entity, Session
from login_page import LoginWindow
from main_page import MainWindow


class Application(Entity):
    def __init__(self, page, report_folder=None):
        super().__init__("Калькулятор")
        self.page = page
        self.session = Session()
        self.report_folder = report_folder if report_folder is not None else Path(__file__).parent / "reports"
        self._closing = False
        self.window = LoginWindow(self)

    @property
    def page(self):
        return self._page

    @page.setter
    def page(self, value):
        if value is None:
            raise ValueError("Страница обязательна")
        self._page = value

    @property
    def window(self):
        return self._window

    @window.setter
    def window(self, value):
        if not isinstance(value, (LoginWindow, MainWindow)):
            raise ValueError("Нужно окно входа или расчёта")
        self._window = value

    @property
    def report_folder(self):
        return self._report_folder

    @report_folder.setter
    def report_folder(self, value):
        self._report_folder = Path(value)

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, value):
        if not isinstance(value, Session):
            raise ValueError("Нужен объект Session")
        self._session = value

    def snapshot(self):
        return (id(self),)

    def build(self):
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.window.prevent_close = True
        self.page.window.on_event = self.close
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.add(self.window)

    def open_main(self, login):
        self.session.name = login
        self.window = MainWindow(self)
        self.page.controls.clear()
        self.page.add(self.window)

    async def close(self, event):
        if event.type != ft.WindowEventType.CLOSE or self._closing:
            return
        self._closing = True
        try:
            if isinstance(self.window, LoginWindow):
                self.session.name = (self.window.login_field.value or "").strip() or "Гость"
            self.session.save(self.report_folder)
        except (OSError, ValueError) as error:
            self._closing = False
            target = self.window.status_text if isinstance(self.window, LoginWindow) else self.window.result_text
            target.value = f"Не удалось сохранить отчёт: {error}"
            self.page.update()
            return
        await self.page.window.destroy()

    @staticmethod
    def main(page):
        Application(page).build()

    def __eq__(self, other):
        return self is other

    def __repr__(self):
        return f"Application(login={self.session.name!r}, window={type(self.window).__name__!r})"

    def __str__(self):
        return f"Калькулятор: {self.session.name}, {type(self.window).__name__}"

    def __len__(self):
        return len(self.page.controls)

    def __bool__(self):
        return True

    def __lt__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        return (self.session.time_in, id(self)) < (other.session.time_in, id(other))


if __name__ == "__main__":
    ft.run(Application.main)
