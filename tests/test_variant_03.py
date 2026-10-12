"""Відкриті тести задачі 3: Зважена матриця рішень.

Запуск: pytest tests/test_variant_03.py
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
        "S1", "weighted_scores",
        (CACHE, CR1),
        {
            "A: без кешу": 0.65,
            "B: кеш у процесі, 60 с": 0.633,
            "C: спільний кеш + подія": 0.637,
        },
    ),
    (
        "S1", "weighted_scores",
        (CACHE, {"latency_ms": (1, "min")}),
        {
            "A: без кешу": 0.0,
            "B: кеш у процесі, 60 с": 1.0,
            "C: спільний кеш + подія": 0.992,
        },
    ),
    (
        "S1", "weighted_scores",
        (CACHE, {"stale_s": (0.5, "min"), "cost": (0.5, "min")}),
        {
            "A: без кешу": 1.0,
            "B: кеш у процесі, 60 с": 0.5,
            "C: спільний кеш + подія": 0.483,
        },
    ),
    (
        "S2", "weighted_scores",
        (AUTH, CR2),
        {
            "P: власні паролі": 0.833,
            "Q: OIDC, зовнішній сервіс": 0.167,
            "R: OIDC + кеш прав": 0.759,
        },
    ),
    (
        "S2", "weighted_scores",
        (AUTH, {"availability_pct": (1, "max")}),
        {
            "P: власні паролі": 1.0,
            "Q: OIDC, зовнішній сервіс": 0.0,
            "R: OIDC + кеш прав": 1.0,
        },
    ),
    (
        "S2", "weighted_scores",
        (AUTH, {"cost": (50, "max"), "latency_ms": (50, "min")}),
        {
            "P: власні паролі": 1.0,
            "Q: OIDC, зовнішній сервіс": 0.0,
            "R: OIDC + кеш прав": 0.592,
        },
    ),
    (
        "S3", "weighted_scores",
        (RECOV, CR3),
        {
            "X: щодобова копія": 0.3,
            "Y: щогодинна копія": 0.723,
            "Z: потокова реплікація": 0.7,
        },
    ),
    (
        "S3", "weighted_scores",
        (
            {"X": {"rpo_min": 10, "ops": 2}, "Y": {"rpo_min": 30, "ops": 2}},
            {"rpo_min": (0.8, "min"), "ops": (0.2, "min")},
        ),
        {"X": 1.0, "Y": 0.2},
    ),
    ("S3", "weighted_scores", ({"X": {"a": 5}}, {"a": (0.4, "min")}), {"X": 1.0}),
]


@pytest.mark.parametrize("tag,func,args,expected", CASES, ids=_ids(CASES, "T03"))
def test_task_03(tag, func, args, expected):
    check(3, func, args, expected)
