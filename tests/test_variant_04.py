"""Відкриті тести задачі 4: Чутливість до ваги критерію.

Запуск: pytest tests/test_variant_04.py
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


TWO = {"P": {"a": 0, "b": 10}, "Q": {"a": 10, "b": 0}}
CR_TWO = {"a": (0.5, "min"), "b": (0.5, "min")}
CACHE = {
    "A: без кешу": {"latency_ms": 2600, "stale_s": 0, "ops": 1, "cost": 40},
    "B: кеш у процесі, 60 с": {"latency_ms": 120, "stale_s": 60, "ops": 2, "cost": 40},
    "C: спільний кеш + подія": {"latency_ms": 140, "stale_s": 2, "ops": 4, "cost": 70},
}
CR1 = {
    "latency_ms": (0.35, "min"),
    "stale_s": (0.3, "min"),
    "ops": (0.2, "min"),
    "cost": (0.15, "min"),
}
AUTH = {
    "P: власні паролі": {"latency_ms": 60, "availability_pct": 99.9, "ops": 4, "cost": 20},
    "Q: OIDC, зовнішній сервіс": {"latency_ms": 250, "availability_pct": 99.5, "ops": 2, "cost": 0},
    "R: OIDC + кеш прав": {"latency_ms": 120, "availability_pct": 99.9, "ops": 3, "cost": 10},
}
CR2 = {"latency_ms": (3, "min"), "availability_pct": (2, "max"), "ops": (1, "min")}
RECOV = {
    "X: щодобова копія": {"rpo_min": 1440, "rto_min": 120, "cost": 15},
    "Y: щогодинна копія": {"rpo_min": 60, "rto_min": 90, "cost": 30},
    "Z: потокова реплікація": {"rpo_min": 1, "rto_min": 10, "cost": 120},
}
CR3 = {"rpo_min": (0.4, "min"), "rto_min": (0.3, "min"), "cost": (0.3, "min")}


CASES = [
    (
        "S1", "sensitivity",
        (TWO, CR_TWO, "a", 2),
        [
            {"weight": 0.0, "winner": "Q"},
            {"weight": 0.5, "winner": "P"},
            {"weight": 1.0, "winner": "P"},
        ],
    ),
    ("S1", "switch_points", (TWO, CR_TWO, "a"), [{"weight": 0.5, "winner": "P"}]),
    (
        "S1", "switch_points",
        (CACHE, CR1, "stale_s"),
        [{"weight": 0.3, "winner": "A: без кешу"}],
    ),
    (
        "S2", "switch_points",
        (AUTH, CR2, "ops"),
        [
            {"weight": 0.3, "winner": "R: OIDC + кеш прав"},
            {"weight": 0.7, "winner": "Q: OIDC, зовнішній сервіс"},
        ],
    ),
    (
        "S2", "sensitivity",
        (
            {"U": {"x": 1, "y": 1}, "V": {"x": 1, "y": 1}},
            {"x": (1, "min"), "y": (1, "min")},
            "x",
            1,
        ),
        [{"weight": 0.0, "winner": "U"}, {"weight": 1.0, "winner": "U"}],
    ),
    (
        "S2", "switch_points",
        (TWO, {"a": (3, "min"), "b": (1, "min")}, "a"),
        [{"weight": 0.5, "winner": "P"}],
    ),
    (
        "S3", "sensitivity",
        (
            RECOV,
            {"rpo_min": (1, "min"), "rto_min": (0, "min"), "cost": (0, "min")},
            "rpo_min",
            2,
        ),
        [
            {"weight": 0.0, "winner": "Y: щогодинна копія"},
            {"weight": 0.5, "winner": "Y: щогодинна копія"},
            {"weight": 1.0, "winner": "Z: потокова реплікація"},
        ],
    ),
    (
        "S3", "switch_points",
        (RECOV, CR3, "cost"),
        [
            {"weight": 0.3, "winner": "Y: щогодинна копія"},
            {"weight": 0.9, "winner": "X: щодобова копія"},
        ],
    ),
    (
        "S3", "sensitivity",
        ({"U": {"x": 5}}, {"x": (1, "min")}, "x", 2),
        [
            {"weight": 0.0, "winner": "U"},
            {"weight": 0.5, "winner": "U"},
            {"weight": 1.0, "winner": "U"},
        ],
    ),
]


@pytest.mark.parametrize("tag,func,args,expected", CASES, ids=_ids(CASES, "T04"))
def test_task_04(tag, func, args, expected):
    check(4, func, args, expected)
