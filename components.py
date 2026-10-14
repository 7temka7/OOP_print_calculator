import flet as ft
from models import Entity


class Control(Entity):
    def snapshot(self):
        return (self.name, id(self))



    def compare(self, other):
        if type(self) is not type(other):
            return NotImplemented
        return (self.name, id(self)) < (other.name, id(other))

    def children(self):
        content = getattr(self, "content", None)
        return (content,) if isinstance(content, ft.Control) else ()

    def describe(self, detail):
        visible = getattr(self, "visible", True)
        disabled = getattr(self, "disabled", False)
        return f"{type(self).__name__}(name={self.name!r}, visible={visible}, disabled={disabled}, {detail})"

    def __eq__(self, other):
        return self is other

    def __repr__(self):
        return self.describe(f"children={len(self.children())}")

    def __str__(self):
        return self.name

    def __len__(self):
        return len(self.children())

    def __bool__(self):
        return True

    def __lt__(self, other):
        return self.compare(other)


class Field(Control, ft.TextField):
    def __init__(self, label):
        ft.TextField.__init__(self, label=label, value="", text_align=ft.TextAlign.CENTER)
        Entity.__init__(self, label)

    def __eq__(self, other):
        return self is other

    def __repr__(self):
        return self.describe(f"label={self.label!r}, value={self.value!r}")

    def __str__(self):
        value = self.value or "—"
        return f"{self.label}: {value}"

    def __len__(self):
        return len(self.value or "")

    def __bool__(self):
        return True

    def __lt__(self, other):
        return self.compare(other)


class LoginField(Field):
    def __init__(self):
        super().__init__("Логин")

    def __eq__(self, other):
        return self is other

    def __repr__(self):
        return self.describe(f"label={self.label!r}, value={self.value!r}")

    def __str__(self):
        value = self.value or "—"
        return f"{self.label}: {value}"

    def __len__(self):
        return len(self.value or "")

    def __bool__(self):
        return True

    def __lt__(self, other):
        return self.compare(other)


class MassField(Field):
    def __init__(self):
        super().__init__("Масса пластика, г")

    def __eq__(self, other):
        return self is other

    def __repr__(self):
        return self.describe(f"label={self.label!r}, value={self.value!r}")

    def __str__(self):
        value = self.value or "—"
        return f"{self.label}: {value}"

    def __len__(self):
        return len(self.value or "")

    def __bool__(self):
        return True

    def __lt__(self, other):
        return self.compare(other)


class PriceField(Field):
    def __init__(self):
        super().__init__("Цена пластика, ₽/кг")

    def __eq__(self, other):
        return self is other

    def __repr__(self):
        return self.describe(f"label={self.label!r}, value={self.value!r}")

    def __str__(self):
        value = self.value or "—"
        return f"{self.label}: {value}"

    def __len__(self):
        return len(self.value or "")

    def __bool__(self):
        return True

    def __lt__(self, other):
        return self.compare(other)


class TimeField(Field):
    def __init__(self):
        super().__init__("Время печати, ч")

    def __eq__(self, other):
        return self is other

    def __repr__(self):
        return self.describe(f"label={self.label!r}, value={self.value!r}")

    def __str__(self):
        value = self.value or "—"
        return f"{self.label}: {value}"

    def __len__(self):
        return len(self.value or "")

    def __bool__(self):
        return True

    def __lt__(self, other):
        return self.compare(other)


class PowerField(Field):
    def __init__(self):
        super().__init__("Мощность принтера, Вт")

    def __eq__(self, other):
        return self is other

    def __repr__(self):
        return self.describe(f"label={self.label!r}, value={self.value!r}")

    def __str__(self):
        value = self.value or "—"
        return f"{self.label}: {value}"

    def __len__(self):
        return len(self.value or "")

    def __bool__(self):
        return True

    def __lt__(self, other):
        return self.compare(other)


class TariffField(Field):
    def __init__(self):
        super().__init__("Тариф электричества, ₽/кВт·ч")

    def __eq__(self, other):
        return self is other

    def __repr__(self):
        return self.describe(f"label={self.label!r}, value={self.value!r}")

    def __str__(self):
        value = self.value or "—"
        return f"{self.label}: {value}"

    def __len__(self):
        return len(self.value or "")

    def __bool__(self):
        return True

    def __lt__(self, other):
        return self.compare(other)


class TitleText(Control, ft.Text):
    def __init__(self):
        ft.Text.__init__(self, value="Расчёт стоимости 3D-печати", text_align=ft.TextAlign.CENTER)
        Entity.__init__(self, "Заголовок")

    def __eq__(self, other):
        return self is other

    def __repr__(self):
        return self.describe(f"value={self.value!r}")

    def __str__(self):
        return self.value or ""

    def __len__(self):
        return len(self.value or "")

    def __bool__(self):
        return True

    def __lt__(self, other):
        return self.compare(other)


class ResultText(Control, ft.Text):
    def __init__(self):
        ft.Text.__init__(self, value="Стоимость: —", text_align=ft.TextAlign.CENTER)
        Entity.__init__(self, "Результат")

    def __eq__(self, other):
        return self is other

    def __repr__(self):
        return self.describe(f"value={self.value!r}")

    def __str__(self):
        return self.value or ""

    def __len__(self):
        return len(self.value or "")

    def __bool__(self):
        return True

    def __lt__(self, other):
        return self.compare(other)


class CalculateButton(Control, ft.Button):
    def __init__(self, handler):
        ft.Button.__init__(self, content="Рассчитать", on_click=handler)
        Entity.__init__(self, "Расчёт")

    def __eq__(self, other):
        return self is other

    def __repr__(self):
        return self.describe(f"content={self.content!r}")

    def __str__(self):
        return str(self.content)

    def __len__(self):
        return len(self.content) if isinstance(self.content, str) else len(self.children())

    def __bool__(self):
        return True

    def __lt__(self, other):
        return self.compare(other)


class ClearButton(Control, ft.Button):
    def __init__(self, handler):
        ft.Button.__init__(self, content="Очистить", on_click=handler)
        Entity.__init__(self, "Очистка")

    def __eq__(self, other):
        return self is other

    def __repr__(self):
        return self.describe(f"content={self.content!r}")

    def __str__(self):
        return str(self.content)

    def __len__(self):
        return len(self.content) if isinstance(self.content, str) else len(self.children())

    def __bool__(self):
        return True

    def __lt__(self, other):
        return self.compare(other)
