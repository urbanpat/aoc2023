from pathlib import Path


def load_data(p: Path) -> list[str]:
    text = p.read_text().split("\n")
    return text[:-1]
