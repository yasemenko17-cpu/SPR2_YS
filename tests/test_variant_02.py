"""Відкриті тести задачі 2: Відсікання за жорсткими обмеженнями.

Запуск: pytest tests/test_variant_02.py
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
AUTH = {
    "P: власні паролі": {"latency_ms": 60, "availability_pct": 99.9, "ops": 4, "cost": 20},
    "Q: OIDC, зовнішній сервіс": {"latency_ms": 250, "availability_pct": 99.5, "ops": 2, "cost": 0},
    "R: OIDC + кеш прав": {"latency_ms": 120, "availability_pct": 99.9, "ops": 3, "cost": 10},
}
RECOV = {
    "X: щодобова копія": {"rpo_min": 1440, "rto_min": 120, "cost": 15},
    "Y: щогодинна копія": {"rpo_min": 60, "rto_min": 90, "cost": 30},
    "Z: потокова реплікація": {"rpo_min": 1, "rto_min": 10, "cost": 120},
}


CASES = [
    (
        "S1", "screen",
        (CACHE, {"latency_ms": ("max", 2000), "stale_s": ("max", 5)}),
        {
            "feasible": ["C: спільний кеш + подія"],
            "violations": {"A: без кешу": ["latency_ms"], "B: кеш у процесі, 60 с": ["stale_s"]},
        },
    ),
    (
        "S1", "screen",
        (CACHE, {"latency_ms": ("max", 200)}),
        {
            "feasible": ["B: кеш у процесі, 60 с", "C: спільний кеш + подія"],
            "violations": {"A: без кешу": ["latency_ms"]},
        },
    ),
    (
        "S1", "screen",
        (CACHE, {}),
        {
            "feasible": ["A: без кешу", "B: кеш у процесі, 60 с", "C: спільний кеш + подія"],
            "violations": {},
        },
    ),
    (
        "S2", "screen",
        (AUTH, {"availability_pct": ("min", 99.9), "latency_ms": ("max", 200)}),
        {
            "feasible": ["P: власні паролі", "R: OIDC + кеш прав"],
            "violations": {"Q: OIDC, зовнішній сервіс": ["availability_pct", "latency_ms"]},
        },
    ),
    (
        "S2", "screen",
        (AUTH, {"availability_pct": ("min", 99.95)}),
        {
            "feasible": [],
            "violations": {
                "P: власні паролі": ["availability_pct"],
                "Q: OIDC, зовнішній сервіс": ["availability_pct"],
                "R: OIDC + кеш прав": ["availability_pct"],
            },
        },
    ),
    (
        "S2", "screen",
        (AUTH, {"cost": ("max", 10), "availability_pct": ("min", 99.5)}),
        {
            "feasible": ["Q: OIDC, зовнішній сервіс", "R: OIDC + кеш прав"],
            "violations": {"P: власні паролі": ["cost"]},
        },
    ),
    (
        "S3", "screen",
        (RECOV, {"rpo_min": ("max", 60)}),
        {
            "feasible": ["Y: щогодинна копія", "Z: потокова реплікація"],
            "violations": {"X: щодобова копія": ["rpo_min"]},
        },
    ),
    (
        "S3", "screen",
        (RECOV, {"rpo_min": ("max", 60), "ops": ("max", 3)}),
        {
            "feasible": [],
            "violations": {
                "X: щодобова копія": ["rpo_min", "ops"],
                "Y: щогодинна копія": ["ops"],
                "Z: потокова реплікація": ["ops"],
            },
        },
    ),
    (
        "S3", "screen",
        (
            {"W": {"rpo_min": None, "rto_min": 5}, "V": {"rpo_min": 30, "rto_min": 5}},
            {"rpo_min": ("max", 60)},
        ),
        {"feasible": ["V"], "violations": {"W": ["rpo_min"]}},
    ),
]


@pytest.mark.parametrize("tag,func,args,expected", CASES, ids=_ids(CASES, "T02"))
def test_task_02(tag, func, args, expected):
    check(2, func, args, expected)
