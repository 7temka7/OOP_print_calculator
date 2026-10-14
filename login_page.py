import flet as ft
from models import Entity
from components import Control, LoginField, TitleText, ResultText, CalculateButton


class LoginWindow(Control, ft.Container):
    def __init__(self, application):
        ft.Container.__init__(self)
        Entity.__init__(self, "Окно входа")
        self.application = application
        self.login_field = LoginField()
        self.status_text = ResultText()
        self.status_text.value = ""
        self.login_button = CalculateButton(self.login)
        self.login_button.content = "Войти"
        self.content = ft.Column(
            controls=[TitleText(), self.login_field, self.login_button, self.status_text],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True,
        )

    @property
    def application(self):
        return self._application

    @application.setter
    def application(self, value):
        if value is None:
            raise ValueError("Приложение обязательно")
        self._application = value

    @property
    def login_field(self):
        return self._login_field

    @login_field.setter
    def login_field(self, value):
        if not isinstance(value, LoginField):
            raise ValueError("Нужно поле логина")
        self._login_field = value

    @property
    def status_text(self):
        return self._status_text

    @status_text.setter
    def status_text(self, value):
        if not isinstance(value, ResultText):
            raise ValueError("Нужен текст сообщения")
        self._status_text = value

    @property
    def login_button(self):
        return self._login_button

    @login_button.setter
    def login_button(self, value):
        if not isinstance(value, CalculateButton):
            raise ValueError("Нужна кнопка входа")
        self._login_button = value

    def login(self, event=None):
        try:
            value = (self.login_field.value or "").strip()
            if not value:
                raise ValueError("Введите логин")
            self.application.open_main(value)
        except ValueError as error:
            self.status_text.value = str(error)
            self.application.page.update()

    def __eq__(self, other):
        return self is other

    def __repr__(self):
        return self.describe(f"login={self.login_field.value!r}")

    def __str__(self):
        login = self.login_field.value or "—"
        return f"Окно входа: {login}"

    def __len__(self):
        return len(self.children())

    def __bool__(self):
        return True

    def __lt__(self, other):
        return self.compare(other)
