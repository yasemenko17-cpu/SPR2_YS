"""Відкриті тести задачі 6: Точки компромісу й конфлікти.

Запуск: pytest tests/test_variant_06.py
Тут лише приклади з карток варіантів; повний набір перевірок є у викладача.
"""
import copy

import pytest
from conftest import load


def _ids(cases, prefix):
    return [f"{prefix}-{c[0]}-{i}" for i, c in enumerate(cases)]


def norm(value):
    """Кортежі й списки порівнюються однаково."""
    if isinstance(value, (list, tuple)):
        return [norm(v) for v in value]
    if isinstance(value, dict):
        return {k: norm(v) for k, v in value.items()}
    return value


def check(number, func, args, expected):
    call = getattr(load(number), func)
    before = copy.deepcopy(args)
    if isinstance(expected, ValueError):
        with pytest.raises(ValueError) as info:
            call(*args)
        assert str(info.value) == str(expected)
    else:
        assert norm(call(*args)) == norm(expected)
    assert args == before, "функція не повинна змінювати вхідні дані"


EFF1 = {
    "Кеш у пам'яті процесу": {"Продуктивність": 2, "Узгодженість": -2, "Вартість": 0},
    "Спільний кеш із подією": {"Продуктивність": 2, "Узгодженість": 1, "Простота": -2},
    "Окрема репліка для читання": {"Продуктивність": 1, "Узгодженість": -1, "Вартість": -2},
    "Більший пул з'єднань": {"Продуктивність": 1},
}
EFF2 = {
    "Власні паролі": {"Безпека": -1, "Доступність": 2, "Простота": -2},
    "Зовнішній сервіс OIDC": {"Безпека": 2, "Доступність": -2, "Простота": 1},
    "Кеш прав на 5 хвилин": {"Доступність": 2, "Безпека": -1, "Продуктивність": 1},
    "Двофакторна автентифікація": {"Безпека": 2, "Зручність": -1},
}
EFF3 = {
    "Щодобова копія": {"Відновлюваність": -2, "Економічність": 2, "Простота": 2},
    "Щогодинна копія": {"Відновлюваність": 1, "Економічність": 1, "Простота": 1},
    "Потокова реплікація": {"Відновлюваність": 2, "Економічність": -2, "Простота": -2},
    "Копія в інше місто": {"Відновлюваність": 1, "Економічність": -1},
}


CASES = [
    (
        "S1", "tradeoff_points",
        (EFF1,),
        [
            {
                "decision": "Кеш у пам'яті процесу",
                "improves": ["Продуктивність"],
                "harms": ["Узгодженість"],
            },
            {
                "decision": "Спільний кеш із подією",
                "improves": ["Продуктивність", "Узгодженість"],
                "harms": ["Простота"],
            },
            {
                "decision": "Окрема репліка для читання",
                "improves": ["Продуктивність"],
                "harms": ["Узгодженість", "Вартість"],
            },
        ],
    ),
    ("S1", "tradeoff_points", ({"Більший пул з'єднань": {"Продуктивність": 1}},), []),
    (
        "S1", "conflicts",
        (EFF1,),
        [
            {
                "attribute": "Узгодженість",
                "improved_by": ["Спільний кеш із подією"],
                "harmed_by": ["Кеш у пам'яті процесу", "Окрема репліка для читання"],
            },
        ],
    ),
    (
        "S2", "tradeoff_points",
        (EFF2, 2),
        [
            {
                "decision": "Власні паролі",
                "improves": ["Доступність"],
                "harms": ["Простота"],
            },
            {
                "decision": "Зовнішній сервіс OIDC",
                "improves": ["Безпека"],
                "harms": ["Доступність"],
            },
        ],
    ),
    ("S2", "tradeoff_points", (EFF2, 3), []),
    (
        "S2", "tradeoff_points",
        (EFF2,),
        [
            {
                "decision": "Власні паролі",
                "improves": ["Доступність"],
                "harms": ["Безпека", "Простота"],
            },
            {
                "decision": "Зовнішній сервіс OIDC",
                "improves": ["Безпека", "Простота"],
                "harms": ["Доступність"],
            },
            {
                "decision": "Кеш прав на 5 хвилин",
                "improves": ["Доступність", "Продуктивність"],
                "harms": ["Безпека"],
            },
            {
                "decision": "Двофакторна автентифікація",
                "improves": ["Безпека"],
                "harms": ["Зручність"],
            },
        ],
    ),
    (
        "S3", "conflicts",
        (EFF3,),
        [
            {
                "attribute": "Відновлюваність",
                "improved_by": ["Щогодинна копія", "Потокова реплікація", "Копія в інше місто"],
                "harmed_by": ["Щодобова копія"],
            },
            {
                "attribute": "Економічність",
                "improved_by": ["Щодобова копія", "Щогодинна копія"],
                "harmed_by": ["Потокова реплікація", "Копія в інше місто"],
            },
            {
                "attribute": "Простота",
                "improved_by": ["Щодобова копія", "Щогодинна копія"],
                "harmed_by": ["Потокова реплікація"],
            },
        ],
    ),
    (
        "S3", "conflicts",
        (EFF3, 2),
        [
            {
                "attribute": "Відновлюваність",
                "improved_by": ["Потокова реплікація"],
                "harmed_by": ["Щодобова копія"],
            },
            {
                "attribute": "Економічність",
                "improved_by": ["Щодобова копія"],
                "harmed_by": ["Потокова реплікація"],
            },
            {
                "attribute": "Простота",
                "improved_by": ["Щодобова копія"],
                "harmed_by": ["Потокова реплікація"],
            },
        ],
    ),
    ("S3", "conflicts", (EFF3, 3), []),
]


@pytest.mark.parametrize("tag,func,args,expected", CASES, ids=_ids(CASES, "T06"))
def test_task_06(tag, func, args, expected):
    check(6, func, args, expected)
