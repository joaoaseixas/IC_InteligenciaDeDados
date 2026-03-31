import json
import re
from pathlib import Path
from config import ARTICLES_DIR, CHECKPOINT_FILE


def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[\s_-]+", "_", text)[:80]


def save_article(article: dict) -> None:
    Path(ARTICLES_DIR).mkdir(parents=True, exist_ok=True)
    slug = _slugify(article.get("title", "artigo"))
    filepath = Path(ARTICLES_DIR) / f"{slug}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(article, f, ensure_ascii=False, indent=2)
    print(f"[SALVO] {filepath}")


def save_index(articles: list[dict]) -> None:
    filepath = Path(ARTICLES_DIR) / "_index.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print(f"[ÍNDICE] {len(articles)} artigos salvos em {filepath}")


# --- Checkpoint ---

def save_checkpoint(page: int, seen_urls: set, collected: list) -> None:
    Path(CHECKPOINT_FILE).parent.mkdir(parents=True, exist_ok=True)
    data = {"last_page": page, "seen_urls": list(seen_urls), "collected": collected}
    with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_checkpoint() -> dict | None:
    path = Path(CHECKPOINT_FILE)
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def clear_checkpoint() -> None:
    path = Path(CHECKPOINT_FILE)
    if path.exists():
        path.unlink()
