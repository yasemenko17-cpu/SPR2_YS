"""Задача 9. Цілісність журналу рішень.

Правила: student.md, розділ «Опис задач», задача 9.
Відкриті тести: pytest tests/test_variant_09.py
"""


def can_transition(old: str, new: str) -> bool:
    """Чи дозволено перехід зі стану old у стан new."""
    raise NotImplementedError  # TODO: реалізуйте за описом задачі


def check_log(records: list) -> list:
    """Перевіряє нумерацію й посилання замінників; повертає список зауважень."""
    raise NotImplementedError  # TODO: реалізуйте за описом задачі


def changed_content(before: dict, after: dict) -> list:
    """Номери записів, зміст яких змінено (без рядків статусу й заміни)."""
    raise NotImplementedError  # TODO: реалізуйте за описом задачі
