from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from functools import total_ordering
from pathlib import Path
from uuid import uuid4


@total_ordering
class Entity(ABC):
    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip() or any(ord(c) < 32 or c == "|" for c in value):
            raise ValueError("Введите имя без переносов строк и символа |")
        self._name = value.strip()

    @abstractmethod
    def snapshot(self):
        pass

    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        return self.snapshot() == other.snapshot()

    def __lt__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        return self.snapshot() < other.snapshot()

    def __repr__(self):
        return f"{type(self).__name__}({self.snapshot()!r})"

    def __str__(self):
        return f"{self.name}: {self.snapshot()}"

    def __len__(self):
        return len(self.snapshot())

    def __bool__(self):
        return len(self) > 0


class Mapping(Entity):
    def __init__(self):
        super().__init__("Данные")
        self._items = []

    @property
    def items(self):
        return tuple(self._items)

    @items.setter
    def items(self, pairs):
        checked = Mapping()
        for key, value in pairs:
            checked[key] = value
        self._items = list(checked.items)

    def snapshot(self):
        return tuple(self._items)

    def __getitem__(self, key):
        for stored, value in self._items:
            if stored == key:
                return value
        raise KeyError(key)

    def __setitem__(self, key, value):
        for index, (stored, _) in enumerate(self._items):
            if stored == key:
                self._items[index] = (key, value)
                return
        self._items.append((key, value))

    def __delitem__(self, key):
        for index, (stored, _) in enumerate(self._items):
            if stored == key:
                del self._items[index]
                return
        raise KeyError(key)

    def __iter__(self):
        return iter(key for key, _ in self._items)

    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        return self.snapshot() == other.snapshot()

    def __repr__(self):
        return f"Mapping(items={self.snapshot()!r})"

    def __str__(self):
        return "; ".join(f"{key}: {value}" for key, value in self._items) or "Пустой маппинг"

    def __len__(self):
        return len(self._items)

    def __bool__(self):
        return len(self._items) > 0

    def __lt__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        return self.snapshot() < other.snapshot()


class PrintData(Entity):
    KEYS = ("mass", "price", "hours", "power", "tariff")

    def __init__(self, values):
        super().__init__("Параметры печати")
        self.values = values

    @property
    def values(self):
        copied = Mapping()
        for key in self.KEYS:
            copied[key] = self._values[key]
        return copied

    @values.setter
    def values(self, source):
        checked = Mapping()
        for key in self.KEYS:
            try:
                value = Decimal(str(source[key]).strip().replace(",", "."))
            except (InvalidOperation, KeyError):
                raise ValueError("Заполните все поля числами") from None
            if not value.is_finite() or not 0 <= value <= 1000000000:
                raise ValueError("Числа должны быть от 0 до 1 000 000 000")
            checked[key] = value
        self._values = checked

    def snapshot(self):
        return tuple(self._values[key] for key in self.KEYS)

    def calculate(self):
        v = self._values
        return Result(v["mass"] / 1000 * v["price"], v["power"] / 1000 * v["hours"] * v["tariff"])

    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        return self.snapshot() == other.snapshot()

    def __repr__(self):
        return f"PrintData(values={self.snapshot()!r})"

    def __str__(self):
        return "; ".join(f"{key}: {self._values[key]}" for key in self.KEYS)

    def __len__(self):
        return len(self.KEYS)

    def __bool__(self):
        return any(value != 0 for value in self.snapshot())

    def __lt__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        return self.snapshot() < other.snapshot()


class Result(Entity):
    def __init__(self, material, electricity):
        super().__init__("Себестоимость")
        self.amounts = (material, electricity)

    @property
    def amounts(self):
        return self._amounts

    @amounts.setter
    def amounts(self, values):
        numbers = tuple(Decimal(str(value)) for value in values)
        if len(numbers) != 2 or any(not n.is_finite() or n < 0 for n in numbers):
            raise ValueError("Нужны две неотрицательные стоимости")
        self._amounts = tuple(n.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) for n in numbers)

    @property
    def total(self):
        return sum(self.amounts, Decimal("0.00"))

    def snapshot(self):
        return (self.total, *self.amounts)

    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        return self.snapshot() == other.snapshot()

    def __repr__(self):
        return f"Result(material={self.amounts[0]!r}, electricity={self.amounts[1]!r})"

    def __str__(self):
        return f"Пластик: {self.amounts[0]:.2f} ₽; электричество: {self.amounts[1]:.2f} ₽; всего: {self.total:.2f} ₽"

    def __len__(self):
        return len(self.amounts)

    def __bool__(self):
        return self.total != 0

    def __lt__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        return self.snapshot() < other.snapshot()


class Session(Entity):
    FORMAT = "%d.%m.%Y %H:%M:%S"

    def __init__(self):
        super().__init__("Гость")
        self._time_out = None
        self.time_in = datetime.now()
        self.time_out = None
        self._path = None

    @property
    def time_in(self):
        return self._time_in

    @time_in.setter
    def time_in(self, value):
        self.validate_time(value)
        if self._time_out is not None and value > self._time_out:
            raise ValueError("Вход не может быть позже выхода")
        self._time_in = value

    @property
    def time_out(self):
        return self._time_out

    @time_out.setter
    def time_out(self, value):
        if value is not None:
            self.validate_time(value)
            if value < self.time_in:
                raise ValueError("Выход не может быть раньше входа")
        self._time_out = value

    @staticmethod
    def validate_time(value):
        if not isinstance(value, datetime) or value.utcoffset() is not None:
            raise ValueError("Нужно локальное datetime без часового пояса")

    def snapshot(self):
        return (self.time_in, self.name, self.time_out is not None, self.time_out or self.time_in)

    def save(self, folder):
        if self._path is not None:
            return self._path
        ended = datetime.now()
        if ended < self.time_in:
            raise ValueError("Выход не может быть раньше входа")
        values = (self.name, self.time_in.strftime(self.FORMAT), ended.strftime(self.FORMAT))
        titles = ("login", "time_in", "time_out")
        widths = [max(len(a), len(b)) for a, b in zip(titles, values)]
        line = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
        header = "| " + " | ".join(v.ljust(w) for v, w in zip(titles, widths)) + " |"
        row = "| " + " | ".join(v.ljust(w) for v, w in zip(values, widths)) + " |"
        folder = Path(folder)
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / f"session_{self.time_in:%Y%m%d_%H%M%S}_{uuid4().hex[:8]}.txt"
        path.write_text("\n".join((line, header, line, row, line)), encoding="utf-8")
        self.time_out, self._path = ended, path
        return path

    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        return self.snapshot() == other.snapshot()

    def __repr__(self):
        return f"Session(login={self.name!r}, time_in={self.time_in!r}, time_out={self.time_out!r})"

    def __str__(self):
        ended = self.time_out.strftime(self.FORMAT) if self.time_out is not None else "сеанс открыт"
        return f"{self.name}: {self.time_in.strftime(self.FORMAT)} — {ended}"

    def __len__(self):
        return 3

    def __bool__(self):
        return self.time_out is None

    def __lt__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        return self.snapshot() < other.snapshot()