"""Відкриті тести задачі 7: Формування тексту ADR.

Запуск: pytest tests/test_variant_07.py
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
        "S1", "render_adr",
        (
            {
                "number": 3,
                "title": "Кеш списку ресурсів у пам'яті процесу",
                "status": "accepted",
                "drivers": ["QAS-PERF-01"],
                "context": "Сторінка зі списком вільних ресурсів відкривається найчастіше й щоразу виконує дорогий запит до бази.",
                "decision": "Ми будемо тримати результат запиту в пам'яті процесу 60 секунд.",
                "consequences": {
                    "positive": ["менше запитів до бази"],
                    "negative": ["студент може бачити застарілий список до хвилини"],
                    "neutral": ["після перезапуску кеш порожній"],
                },
            },
        ),
        """# ADR 3. Кеш списку ресурсів у пам'яті процесу

Статус: Прийнято
Драйвери: QAS-PERF-01

## Контекст
Сторінка зі списком вільних ресурсів відкривається найчастіше й щоразу виконує дорогий запит до бази.

## Рішення
Ми будемо тримати результат запиту в пам'яті процесу 60 секунд.

## Наслідки
Позитивні: менше запитів до бази.
Негативні: студент може бачити застарілий список до хвилини.
Нейтральні: після перезапуску кеш порожній.
""",
    ),
    (
        "S1", "render_adr",
        (
            {
                "number": 1,
                "title": "Журнал рішень",
                "status": "accepted",
                "context": "  Втрачається причина рішень.  ",
                "decision": "Ми будемо вести журнал.",
                "consequences": {"positive": ["a", "b"], "negative": ["c"]},
            },
        ),
        """# ADR 1. Журнал рішень

Статус: Прийнято

## Контекст
Втрачається причина рішень.

## Рішення
Ми будемо вести журнал.

## Наслідки
Позитивні: a; b.
Негативні: c.
""",
    ),
    (
        "S1", "render_adr",
        (
            {
                "number": 1,
                "title": "Журнал рішень",
                "status": "accepted",
                "context": "  Втрачається причина рішень.  ",
                "decision": "Ми будемо вести журнал.",
                "consequences": {"positive": [], "negative": ["c"], "neutral": []},
            },
        ),
        """# ADR 1. Журнал рішень

Статус: Прийнято

## Контекст
Втрачається причина рішень.

## Рішення
Ми будемо вести журнал.

## Наслідки
Негативні: c.
""",
    ),
    (
        "S2", "render_adr",
        (
            {
                "number": 2,
                "title": "Автентифікація через OIDC",
                "status": "proposed",
                "drivers": ["QAS-SEC-01", "QAS-REL-01"],
                "context": "Потрібно захистити чуже резервування.",
                "decision": "Ми будемо перевіряти особу через зовнішній сервіс.",
                "consequences": {
                    "positive": ["немає власних паролів"],
                    "negative": ["залежність від чужої доступності"],
                },
            },
        ),
        """# ADR 2. Автентифікація через OIDC

Статус: Запропоновано
Драйвери: QAS-SEC-01, QAS-REL-01

## Контекст
Потрібно захистити чуже резервування.

## Рішення
Ми будемо перевіряти особу через зовнішній сервіс.

## Наслідки
Позитивні: немає власних паролів.
Негативні: залежність від чужої доступності.
""",
    ),
    (
        "S2", "render_adr",
        (
            {
                "number": 7,
                "title": "GraphQL",
                "status": "rejected",
                "drivers": [],
                "context": "Потрібно захистити чуже резервування.",
                "decision": "Ми не будемо переходити на GraphQL.",
                "consequences": {
                    "negative": ["клієнти лишаються на REST"],
                    "neutral": ["схему не потрібно супроводжувати"],
                },
            },
        ),
        """# ADR 7. GraphQL

Статус: Відхилено

## Контекст
Потрібно захистити чуже резервування.

## Рішення
Ми не будемо переходити на GraphQL.

## Наслідки
Негативні: клієнти лишаються на REST.
Нейтральні: схему не потрібно супроводжувати.
""",
    ),
    (
        "S2", "render_adr",
        (
            {
                "number": 4,
                "title": "Черга",
                "status": "deprecated",
                "context": "  Втрачається причина рішень.  ",
                "decision": "Ми будемо вести журнал.",
                "consequences": {"positive": ["a", "b"], "negative": ["c"]},
            },
        ),
        """# ADR 4. Черга

Статус: Застаріло

## Контекст
Втрачається причина рішень.

## Рішення
Ми будемо вести журнал.

## Наслідки
Позитивні: a; b.
Негативні: c.
""",
    ),
    (
        "S3", "render_adr",
        (
            {
                "number": 5,
                "title": "Спільний кеш із інвалідацією",
                "status": "superseded",
                "superseded_by": 9,
                "supersedes": 3,
                "drivers": ["QAS-PERF-01", "QAS-CONS-01"],
                "context": "Кеш у процесі порушує QAS-CONS-01.",
                "decision": "Ми будемо тримати спільний кеш.",
                "consequences": {"negative": ["ще один компонент"]},
            },
        ),
        """# ADR 5. Спільний кеш із інвалідацією

Статус: Замінено ADR 9
Замінює: ADR 3
Драйвери: QAS-PERF-01, QAS-CONS-01

## Контекст
Кеш у процесі порушує QAS-CONS-01.

## Рішення
Ми будемо тримати спільний кеш.

## Наслідки
Негативні: ще один компонент.
""",
    ),
    (
        "S3", "render_adr",
        (
            {
                "number": 5,
                "title": "Спільний кеш із інвалідацією",
                "status": "superseded",
                "superseded_by": None,
                "supersedes": 3,
                "drivers": ["QAS-PERF-01", "QAS-CONS-01"],
                "context": "Кеш у процесі порушує QAS-CONS-01.",
                "decision": "Ми будемо тримати спільний кеш.",
                "consequences": {"negative": ["ще один компонент"]},
            },
        ),
        ValueError("Не вказано замінник"),
    ),
    (
        "S3", "render_adr",
        (
            {
                "number": 5,
                "title": "Спільний кеш із інвалідацією",
                "status": "draft",
                "superseded_by": 9,
                "supersedes": 3,
                "drivers": ["QAS-PERF-01", "QAS-CONS-01"],
                "context": "Кеш у процесі порушує QAS-CONS-01.",
                "decision": "Ми будемо тримати спільний кеш.",
                "consequences": {"negative": ["ще один компонент"]},
            },
        ),
        ValueError("Невідомий статус: draft"),
    ),
]


@pytest.mark.parametrize("tag,func,args,expected", CASES, ids=_ids(CASES, "T07"))
def test_task_07(tag, func, args, expected):
    check(7, func, args, expected)
