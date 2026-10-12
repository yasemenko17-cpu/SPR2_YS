"""Відкриті тести задачі 5: Фронт Парето.

Запуск: pytest tests/test_variant_05.py
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
DIR1 = {"latency_ms": "min", "stale_s": "min", "ops": "min", "cost": "min"}
CACHE_D = {
    "A: без кешу": {"latency_ms": 2600, "stale_s": 0, "ops": 1, "cost": 40},
    "B: кеш у процесі, 60 с": {"latency_ms": 120, "stale_s": 60, "ops": 2, "cost": 40},
    "C: спільний кеш + подія": {"latency_ms": 140, "stale_s": 2, "ops": 4, "cost": 70},
    "D: кеш у процесі, 300 с": {"latency_ms": 120, "stale_s": 300, "ops": 2, "cost": 40},
}
AUTH = {
    "P: власні паролі": {"latency_ms": 60, "availability_pct": 99.9, "ops": 4, "cost": 20},
    "Q: OIDC, зовнішній сервіс": {"latency_ms": 250, "availability_pct": 99.5, "ops": 2, "cost": 0},
    "R: OIDC + кеш прав": {"latency_ms": 120, "availability_pct": 99.9, "ops": 3, "cost": 10},
}
DIR2 = {"latency_ms": "min", "availability_pct": "max", "ops": "min", "cost": "min"}
AUTH_S = {
    "P: власні паролі": {"latency_ms": 60, "availability_pct": 99.9, "ops": 4, "cost": 20},
    "Q: OIDC, зовнішній сервіс": {"latency_ms": 250, "availability_pct": 99.5, "ops": 2, "cost": 0},
    "R: OIDC + кеш прав": {"latency_ms": 120, "availability_pct": 99.9, "ops": 3, "cost": 10},
    "S: OIDC без кешу, гірший": {"latency_ms": 250, "availability_pct": 99.5, "ops": 3, "cost": 10},
}
TIES = {"U": {"a": 1, "b": 2}, "V": {"a": 1, "b": 2}, "W": {"a": 2, "b": 1}}
DAB = {"a": "min", "b": "min"}
TIES_T = {
    "U": {"a": 1, "b": 2},
    "V": {"a": 1, "b": 2},
    "W": {"a": 2, "b": 1},
    "T": {"a": 0, "b": 0},
}


CASES = [
    (
        "S1", "pareto_front",
        (CACHE, DIR1),
        ["A: без кешу", "B: кеш у процесі, 60 с", "C: спільний кеш + подія"],
    ),
    (
        "S1", "explain",
        (CACHE_D, DIR1),
        {"D: кеш у процесі, 300 с": ["B: кеш у процесі, 60 с"]},
    ),
    (
        "S1", "pareto_front",
        (CACHE_D, DIR1),
        ["A: без кешу", "B: кеш у процесі, 60 с", "C: спільний кеш + подія"],
    ),
    (
        "S1", "pareto_front",
        (CACHE, {"latency_ms": "min", "cost": "min"}),
        ["B: кеш у процесі, 60 с"],
    ),
    (
        "S2", "pareto_front",
        (AUTH, DIR2),
        ["P: власні паролі", "Q: OIDC, зовнішній сервіс", "R: OIDC + кеш прав"],
    ),
    (
        "S2", "explain",
        (AUTH_S, DIR2),
        {
            "S: OIDC без кешу, гірший": ["Q: OIDC, зовнішній сервіс", "R: OIDC + кеш прав"],
        },
    ),
    (
        "S2", "pareto_front",
        (AUTH, {"availability_pct": "max", "cost": "min"}),
        ["Q: OIDC, зовнішній сервіс", "R: OIDC + кеш прав"],
    ),
    ("S3", "pareto_front", (TIES, DAB), ["U", "V", "W"]),
    ("S3", "explain", (TIES_T, DAB), {"U": ["T"], "V": ["T"], "W": ["T"]}),
    ("S3", "pareto_front", (TIES_T, DAB), ["T"]),
]


@pytest.mark.parametrize("tag,func,args,expected", CASES, ids=_ids(CASES, "T05"))
def test_task_05(tag, func, args, expected):
    check(5, func, args, expected)
