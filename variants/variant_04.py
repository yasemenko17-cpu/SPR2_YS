"""Задача 4. Чутливість до ваги критерію.

Правила: student.md, розділ «Опис задач», задача 4.
Відкриті тести: pytest tests/test_variant_04.py
"""


def sensitivity(options: dict, criteria: dict, pivot: str, steps: int = 10) -> list:
    """Переможець для ваги опорного критерію від 0 до 1 із кроком 1/steps."""
    raise NotImplementedError  # TODO: реалізуйте за описом задачі


def switch_points(options: dict, criteria: dict, pivot: str, steps: int = 10) -> list:
    """Точки, у яких переможець змінюється."""
    raise NotImplementedError  # TODO: реалізуйте за описом задачі
