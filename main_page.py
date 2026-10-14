from decimal import DecimalException
import flet as ft
from models import Entity, Mapping, PrintData
from components import Control, MassField, PriceField, TimeField, PowerField, TariffField, TitleText, ResultText, CalculateButton, ClearButton


class MainWindow(Control, ft.Container):
    def __init__(self, application):
        ft.Container.__init__(self)
        Entity.__init__(self, "Главное окно")
        self.application = application
        self.fields = Mapping()
        for key, field in zip(PrintData.KEYS, (MassField(), PriceField(), TimeField(), PowerField(), TariffField())):
            self.fields[key] = field
        self.result_text = ResultText()
        self.content = ft.Column(
            controls=[
                TitleText(), *[self.fields[key] for key in self.fields],
                ft.Row(
                    controls=[CalculateButton(self.calculate), ClearButton(self.clear)],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                self.result_text,
            ],
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
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, value):
        if not isinstance(value, Mapping):
            raise ValueError("Нужен маппинг полей")
        self._fields = value

    @property
    def result_text(self):
        return self._result_text

    @result_text.setter
    def result_text(self, value):
        if not isinstance(value, ResultText):
            raise ValueError("Нужен текст результата")
        self._result_text = value

    def calculate(self, event=None):
        self.result_text.value = "Стоимость: —"
        try:
            values = Mapping()
            for key in self.fields:
                values[key] = self.fields[key].value
            self.result_text.value = str(PrintData(values).calculate())
        except (ValueError, DecimalException) as error:
            self.result_text.value = str(error)
        self.application.page.update()

    def clear(self, event=None):
        for key in self.fields:
            self.fields[key].value = ""
        self.result_text.value = "Стоимость: —"
        self.application.page.update()

    def __eq__(self, other):
        return self is other

    def __repr__(self):
        return self.describe(f"fields={len(self.fields)}, result={self.result_text.value!r}")

    def __str__(self):
        return f"Калькулятор: {self.result_text.value}"

    def __len__(self):
        return len(self.children())

    def __bool__(self):
        return True

    def __lt__(self, other):
        return self.compare(other)
