"""Задача 6. Точки компромісу й конфлікти.

Правила: student.md, розділ «Опис задач», задача 6.
Відкриті тести: pytest tests/test_variant_06.py
"""


def tradeoff_points(effects: dict, min_delta: int = 1) -> list:
    """Рішення, що водночас поліпшують і погіршують якості."""
    raise NotImplementedError  # TODO: реалізуйте за описом задачі


def conflicts(effects: dict, min_delta: int = 1) -> list:
    """Якості, які одні рішення поліпшують, а інші погіршують."""
    raise NotImplementedError  # TODO: реалізуйте за описом задачі
