def to_tsvector(*columns: str, lang: str) -> str:
    s = " || ' ' || ".join(columns)
    return f"to_tsvector('{lang}', {s})"
