def lint_adr(text: str, known_drivers=None) -> list:
    """
    Рев'ю якості запису ADR у форматі Нюгарда за 7 правилами.
    """
    lines = text.splitlines()
    metadata = {}
    sections = {}
    current_section = None
    section_lines = []
    in_sections = False

    # Розбір тексту на метадані та розділи
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## "):
            if current_section:
                sections[current_section] = "\n".join(section_lines).strip()
            current_section = stripped[3:].strip()
            section_lines = []
            in_sections = True
            continue
        
        if not in_sections:
            if ":" in stripped:
                parts = stripped.split(":", 1)
                key = parts[0].strip().lower()
                val = parts[1].strip()
                metadata[key] = val
        else:
            section_lines.append(line)
            
    if current_section:
        sections[current_section] = "\n".join(section_lines).strip()

    warnings = []

    # Правило 1: Перевірка наявності обов'язкових розділів у правильному порядку
    for sec_name in ["Контекст", "Рішення", "Наслідки"]:
        if sec_name not in sections:
            warnings.append(f"немає розділу «{sec_name}»")

    # Правило 2: Перевірка наявності рядка статусу
    has_status = any(k in metadata for k in ["статус", "status"])
    if not has_status:
        warnings.append("немає рядка «Статус»")

    # Правило 3: Активний стан у розділі «Рішення»
    if "Рішення" in sections and sections["Рішення"]:
        dec_text = sections["Рішення"]
        allowed_prefixes = ("Ми будемо", "Ми не будемо", "Ми залишимо")
        if not dec_text.startswith(allowed_prefixes):
            warnings.append("рішення не починається з «Ми …» (активний стан)")

    # Правило 4: Наявність підрядків Позитивні: та Негативні: у наслідках
    if "Наслідки" in sections and sections["Наслідки"]:
        cons_text = sections["Наслідки"]
        for label in ["Позитивні", "Негативні"]:
            if f"{label}:" not in cons_text:
                warnings.append(f"у наслідках немає рядка «{label}:»")

    # Правило 5: Перевірка невимірних слів у рішенні
    unmeasurable = ["швидко", "зручно", "надійно", "безпечно", "добре", "якісно"]
    if "Рішення" in sections:
        dec_lower = sections["Рішення"].lower()
        for word in unmeasurable:
            if word in dec_lower:
                warnings.append(f"невимірне слово «{word}» у рішенні")

    # Правило 6: Довжина контексту (менше 15 слів)
    if "Контекст" in sections:
        ctx_words = sections["Контекст"].split()
        if len(ctx_words) < 15:
            warnings.append("контекст закороткий (менше 15 слів)")

    # Правило 7: Перевірка драйверів
    if known_drivers is not None:
        has_drivers = any(k in metadata for k in ["драйвери", "drivers"])
        if not has_drivers:
            warnings.append("немає рядка «Драйвери»")
        else:
            drv_str = metadata.get("драйвери") or metadata.get("drivers", "")
            drv_list = [d.strip() for d in drv_str.split(",") if d.strip()]
            for d in drv_list:
                if d not in known_drivers:
                    warnings.append(f"невідомий драйвер «{d}»")

    return warnings