"""Відкриті тести задачі 10: Простежуваність рішень і сценаріїв.

Запуск: pytest tests/test_variant_10.py
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


KNOWN = ["QAS-PERF-01", "QAS-CONS-01", "QAS-SEC-01", "QAS-REL-01", "QAS-REC-01"]
LOG = [
    {"number": 1, "status": "accepted", "drivers": ["процес"]},
    {"number": 2, "status": "accepted", "drivers": ["QAS-CONS-01"]},
    {"number": 3, "status": "superseded", "drivers": ["QAS-PERF-01"]},
    {"number": 4, "status": "accepted", "drivers": ["QAS-SEC-01", "QAS-REL-01"]},
    {"number": 5, "status": "accepted", "drivers": ["QAS-PERF-01", "QAS-CONS-01"]},
    {"number": 6, "status": "proposed", "drivers": ["QAS-PERF-01"]},
    {"number": 7, "status": "rejected", "drivers": ["QAS-PERF-01"]},
]


CASES = [
    (
        "S1", "trace_coverage",
        (KNOWN, LOG),
        {
            "covered": {
                "QAS-PERF-01": [5],
                "QAS-CONS-01": [2, 5],
                "QAS-SEC-01": [4],
                "QAS-REL-01": [4],
            },
            "uncovered": ["QAS-REC-01"],
            "pending": {},
            "orphans": [],
        },
    ),
    (
        "S1", "trace_coverage",
        (KNOWN, []),
        {"covered": {}, "uncovered": KNOWN, "pending": {}, "orphans": []},
    ),
    (
        "S1", "trace_coverage",
        (
            ["QAS-PERF-01"],
            [
                {"number": 2, "status": "accepted", "drivers": ["QAS-PERF-01"]},
                {"number": 1, "status": "accepted", "drivers": ["QAS-PERF-01"]},
            ],
        ),
        {
            "covered": {"QAS-PERF-01": [1, 2]},
            "uncovered": [],
            "pending": {},
            "orphans": [],
        },
    ),
    (
        "S2", "trace_coverage",
        (
            KNOWN,
            [
                {"number": 1, "status": "accepted", "drivers": ["процес"]},
                {"number": 2, "status": "accepted", "drivers": ["QAS-CONS-01"]},
                {"number": 3, "status": "superseded", "drivers": ["QAS-PERF-01"]},
                {
                    "number": 4,
                    "status": "accepted",
                    "drivers": ["QAS-SEC-01", "QAS-REL-01"],
                },
                {
                    "number": 5,
                    "status": "accepted",
                    "drivers": ["QAS-PERF-01", "QAS-CONS-01"],
                },
                {"number": 6, "status": "proposed", "drivers": ["QAS-PERF-01"]},
                {"number": 7, "status": "rejected", "drivers": ["QAS-PERF-01"]},
                {"number": 8, "status": "proposed", "drivers": ["QAS-REC-01"]},
            ],
        ),
        {
            "covered": {
                "QAS-PERF-01": [5],
                "QAS-CONS-01": [2, 5],
                "QAS-SEC-01": [4],
                "QAS-REL-01": [4],
            },
            "uncovered": ["QAS-REC-01"],
            "pending": {"QAS-REC-01": [8]},
            "orphans": [],
        },
    ),
    (
        "S2", "trace_coverage",
        (
            KNOWN,
            [
                {"number": 1, "status": "deprecated", "drivers": ["QAS-SEC-01"]},
                {"number": 2, "status": "rejected", "drivers": ["QAS-SEC-01"]},
                {"number": 3, "status": "superseded", "drivers": ["QAS-SEC-01"]},
            ],
        ),
        {"covered": {}, "uncovered": KNOWN, "pending": {}, "orphans": []},
    ),
    (
        "S2", "trace_coverage",
        (
            ["QAS-SEC-01"],
            [
                {"number": 1, "status": "proposed", "drivers": ["QAS-SEC-01"]},
                {"number": 2, "status": "proposed", "drivers": ["QAS-SEC-01"]},
            ],
        ),
        {
            "covered": {},
            "uncovered": ["QAS-SEC-01"],
            "pending": {"QAS-SEC-01": [1, 2]},
            "orphans": [],
        },
    ),
    (
        "S3", "trace_coverage",
        (
            KNOWN,
            [
                {"number": 1, "status": "accepted", "drivers": ["QAS-XXX-99"]},
                {"number": 2, "status": "accepted", "drivers": []},
            ],
        ),
        {"covered": {}, "uncovered": KNOWN, "pending": {}, "orphans": [1, 2]},
    ),
    (
        "S3", "trace_coverage",
        (
            KNOWN,
            [
                {"number": 1, "status": "accepted", "drivers": ["процес"]},
                {"number": 2, "status": "accepted", "drivers": ["процес", "QAS-SEC-01"]},
            ],
        ),
        {
            "covered": {"QAS-SEC-01": [2]},
            "uncovered": ["QAS-PERF-01", "QAS-CONS-01", "QAS-REL-01", "QAS-REC-01"],
            "pending": {},
            "orphans": [],
        },
    ),
    (
        "S3", "trace_coverage",
        (
            ["QAS-SEC-01"],
            [
                {
                    "number": 1,
                    "status": "accepted",
                    "drivers": ["QAS-SEC-01", "QAS-SEC-01"],
                },
            ],
        ),
        {"covered": {"QAS-SEC-01": [1]}, "uncovered": [], "pending": {}, "orphans": []},
    ),
]


@pytest.mark.parametrize("tag,func,args,expected", CASES, ids=_ids(CASES, "T10"))
def test_task_10(tag, func, args, expected):
    check(10, func, args, expected)
