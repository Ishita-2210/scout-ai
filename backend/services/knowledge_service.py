"""Read-only retrieval over bundled PDFs. No remote embeddings or index mutation."""

import logging
import re
from functools import lru_cache
from pathlib import Path

from pypdf import PdfReader

logger = logging.getLogger(__name__)
KNOWLEDGE = Path(__file__).resolve().parent.parent / "knowledge"
FOLDERS = {"school": "schools", "scholarship": "scholarships"}


@lru_cache(maxsize=6)
def chunks(domain: str) -> tuple[tuple[str, str], ...]:
    results = []
    for path in sorted((KNOWLEDGE / FOLDERS.get(domain, domain)).glob("*.pdf")):
        try:
            if path.stat().st_size > 20_000_000:
                continue
            reader = PdfReader(path)
            for number, page in enumerate(reader.pages[:100], 1):
                text = (page.extract_text() or "")[:20000]
                results.extend(
                    (f"{path.name}, page {number}", text[i : i + 1200]) for i in range(0, len(text), 1000)
                )
        except Exception:
            logger.warning("knowledge category=unreadable_pdf file=%s", path.name)
    return tuple(results)


def retrieve(query: str, domain: str) -> tuple[str, list[str]]:
    words = set(re.findall(r"\w{3,}", query.lower())) - {"the", "and", "for", "with", "need", "help"}
    ranked = sorted(
        (
            (len(words & set(re.findall(r"\w{3,}", text.lower()))), name, text)
            for name, text in chunks(domain)
        ),
        reverse=True,
    )
    selected = [(name, text) for score, name, text in ranked[:2] if score >= 2]
    return "\n\n".join(f"[{name}]\n{text}" for name, text in selected), list(
        dict.fromkeys(name for name, _ in selected)
    )
