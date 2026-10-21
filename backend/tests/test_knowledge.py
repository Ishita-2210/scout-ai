from pathlib import Path

import pytest

from backend.memory.models import MemoryUpdate
from backend.rag.chunker import SemanticChunker
from backend.rag.models import SourceDocument
from backend.services.knowledge_service import retrieve


def test_bundled_pdf_retrieval_is_real_and_bounded():
    text, refs = retrieve("school admission children education", "school")
    assert text and refs
    assert len(text) < 2600 and len(refs) <= 2
    assert all(".pdf, page " in name for name in refs)


def test_chunker_prevents_invalid_overlap_and_does_not_loop():
    with pytest.raises(ValueError):
        SemanticChunker(chunk_size=100, overlap=100)
    chunker = SemanticChunker(chunk_size=100, overlap=90)
    doc = SourceDocument(id="test", title="test", source=Path("test.pdf"), text="word " * 100)
    chunks = chunker.chunk_document(doc)
    assert len(chunks) < 60
    assert all(len(chunk.text) <= 100 for chunk in chunks)


def test_profile_fields_are_bounded():
    with pytest.raises(ValueError):
        MemoryUpdate(name="x" * 301)
