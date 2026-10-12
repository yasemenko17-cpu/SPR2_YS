# Стартовий проєкт SIS-P02

1. Відкрийте проєкт у GitHub Codespaces (Code → Codespaces → Create codespace) або локально: `python3 -m venv .venv`, `source .venv/bin/activate` (у Windows: `.venv\Scripts\activate`), `pip install -r requirements.txt`.
2. Визначте свою задачу за номером варіанта: задача = `(номер - 1) // 3 + 1`, набір = `(номер - 1) % 3 + 1`. Реалізуйте задачу у файлі `variants/variant_NN.py` за карткою.
3. Запускайте відкриті тести своєї задачі: `pytest tests/test_variant_NN.py` (NN з двома цифрами). Права адміністратора не потрібні.
4. Змінюйте лише свій файл у `variants/`, файл `tests/test_my.py` і свій ADR у теці `adr/`.
5. Дані кейсу каталогу ресурсів лежать у `data/`: сценарії якості `qas.json` і три кейси `case_1_cache.json`, `case_2_auth.json`, `case_3_recovery.json`. Шаблон ADR: `adr/0000-template.md`.
