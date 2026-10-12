"""Відкриті тести задачі 1: Розбір ADR.

Запуск: pytest tests/test_variant_01.py
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
    (
        "S1", "parse_adr",
        (
            """# ADR 3. Кеш списку ресурсів у пам'яті процесу

Статус: Прийнято
Драйвери: QAS-PERF-01

## Контекст
Сторінка зі списком вільних ресурсів відкривається найчастіше.

## Рішення
Ми будемо тримати список у пам'яті процесу 60 секунд.

## Наслідки
Позитивні: менше запитів до бази.
Негативні: список може бути застарілим до хвилини.
""",
        ),
        {
            "number": 3,
            "title": "Кеш списку ресурсів у пам'яті процесу",
            "status": "accepted",
            "superseded_by": None,
            "supersedes": None,
            "drivers": ["QAS-PERF-01"],
            "sections": {
                "Контекст": "Сторінка зі списком вільних ресурсів відкривається найчастіше.",
                "Рішення": "Ми будемо тримати список у пам'яті процесу 60 секунд.",
                "Наслідки": """Позитивні: менше запитів до бази.
Негативні: список може бути застарілим до хвилини.""",
            },
        },
    ),
    (
        "S1", "parse_adr",
        (
            """# ADR 2. PostgreSQL як єдине сховище

Статус: Запропоновано
Драйвери: QAS-CONS-01, QAS-REC-01

## Контекст
Резервування змінюють кілька користувачів одночасно.
Два студенти не повинні отримати один слот.

## Рішення
Ми будемо зберігати все в одній базі.
""",
        ),
        {
            "number": 2,
            "title": "PostgreSQL як єдине сховище",
            "status": "proposed",
            "superseded_by": None,
            "supersedes": None,
            "drivers": ["QAS-CONS-01", "QAS-REC-01"],
            "sections": {
                "Контекст": """Резервування змінюють кілька користувачів одночасно.
Два студенти не повинні отримати один слот.""",
                "Рішення": "Ми будемо зберігати все в одній базі.",
            },
        },
    ),
    (
        "S1", "parse_adr",
        (
            """# ADR 1. Журнал рішень

Статус: Відхилено

## Рішення
Ми не будемо вести журнал.
""",
        ),
        {
            "number": 1,
            "title": "Журнал рішень",
            "status": "rejected",
            "superseded_by": None,
            "supersedes": None,
            "drivers": [],
            "sections": {"Рішення": "Ми не будемо вести журнал."},
        },
    ),
    (
        "S2", "parse_adr",
        (
            """# ADR 3. Кеш

Статус: Замінено ADR 5

## Рішення
Ми будемо діяти.
""",
        ),
        {
            "number": 3,
            "title": "Кеш",
            "status": "superseded",
            "superseded_by": 5,
            "supersedes": None,
            "drivers": [],
            "sections": {"Рішення": "Ми будемо діяти."},
        },
    ),
    (
        "S2", "parse_adr",
        (
            """# ADR 5. Спільний кеш

Статус: Прийнято
Замінює: ADR 3
Драйвери: QAS-PERF-01, QAS-CONS-01

## Рішення
Ми будемо діяти.
""",
        ),
        {
            "number": 5,
            "title": "Спільний кеш",
            "status": "accepted",
            "superseded_by": None,
            "supersedes": 3,
            "drivers": ["QAS-PERF-01", "QAS-CONS-01"],
            "sections": {"Рішення": "Ми будемо діяти."},
        },
    ),
    (
        "S2", "parse_adr",
        (
            """# ADR 6. Черга

Статус: Скасовано

## Рішення
Ми будемо діяти.
""",
        ),
        ValueError("Невідомий статус: Скасовано"),
    ),
    (
        "S3", "parse_adr",
        (
            """---
status: accepted
decision-makers: команда
---

# Use dashes in filenames

## Context and Problem Statement
Which filename style should we use?

## Considered Options
```text
## це не заголовок
```
* dashes

## Decision Outcome
Chosen option: dashes.
""",
            "0005-use-dashes-in-filenames.md",
        ),
        {
            "number": 5,
            "title": "Use dashes in filenames",
            "status": "accepted",
            "superseded_by": None,
            "supersedes": None,
            "drivers": [],
            "sections": {
                "Context and Problem Statement": "Which filename style should we use?",
                "Considered Options": '```text\n## це не заголовок\n```\n* dashes',
                "Decision Outcome": "Chosen option: dashes.",
            },
        },
    ),
    (
        "S3", "parse_adr",
        (
            """---
status: superseded by ADR-0008
---

# Add status field

## Decision Outcome
Chosen.
""",
            "0004-add-status-field.md",
        ),
        {
            "number": 4,
            "title": "Add status field",
            "status": "superseded",
            "superseded_by": 8,
            "supersedes": None,
            "drivers": [],
            "sections": {"Decision Outcome": "Chosen."},
        },
    ),
    (
        "S3", "parse_adr",
        (
            """---
status: superseded by ADR-0008
---

# Add status field

## Decision Outcome
Chosen.
""",
        ),
        {
            "number": None,
            "title": "Add status field",
            "status": "superseded",
            "superseded_by": 8,
            "supersedes": None,
            "drivers": [],
            "sections": {"Decision Outcome": "Chosen."},
        },
    ),
]


@pytest.mark.parametrize("tag,func,args,expected", CASES, ids=_ids(CASES, "T01"))
def test_task_01(tag, func, args, expected):
    check(1, func, args, expected)
