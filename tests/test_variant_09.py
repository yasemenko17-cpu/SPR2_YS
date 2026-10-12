"""Відкриті тести задачі 9: Цілісність журналу рішень.

Запуск: pytest tests/test_variant_09.py
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





CASES = [
    ("S1", "can_transition", ("proposed", "accepted"), True),
    ("S1", "can_transition", ("accepted", "superseded"), True),
    ("S1", "can_transition", ("accepted", "proposed"), False),
    ("S1", "can_transition", ("rejected", "accepted"), False),
    (
        "S2", "check_log",
        (
            [
                {"number": 1, "status": "accepted"},
                {"number": 2, "status": "superseded", "superseded_by": 3},
                {"number": 3, "status": "accepted", "supersedes": 2},
            ],
        ),
        [],
    ),
    (
        "S2", "check_log",
        ([{"number": 1, "status": "accepted"}, {"number": 3, "status": "proposed"}],),
        ["порушена послідовність номерів: [1, 3]"],
    ),
    (
        "S2", "check_log",
        ([{"number": 1, "status": "superseded", "superseded_by": 4}],),
        ["ADR 1: замінник ADR 4 не існує"],
    ),
    (
        "S2", "check_log",
        (
            [
                {"number": 1, "status": "superseded", "superseded_by": 2},
                {"number": 2, "status": "accepted"},
            ],
        ),
        ["ADR 1: ADR 2 не вказує, що замінює його"],
    ),
    ("S3", "changed_content", ({1: 'A\n'}, {1: 'A\n'}), []),
    (
        "S3", "changed_content",
        (
            {
                4: """# ADR 4. Облікові записи

Статус: Прийнято

## Рішення
Ми будемо використовувати OIDC.
""",
            },
            {
                4: """# ADR 4. Облікові записи

Статус: Прийнято

## Рішення
Ми будемо зберігати паролі.
""",
            },
        ),
        [4],
    ),
    (
        "S3", "changed_content",
        (
            {
                6: """# ADR 6. Черга

Статус: Запропоновано

## Рішення
Ми будемо.
""",
            },
            {
                6: """# ADR 6. Черга

Статус: Прийнято

## Рішення
Ми будемо.
""",
            },
        ),
        [],
    ),
]


@pytest.mark.parametrize("tag,func,args,expected", CASES, ids=_ids(CASES, "T09"))
def test_task_09(tag, func, args, expected):
    check(9, func, args, expected)
