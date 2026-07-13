from __future__ import annotations

import re
from collections.abc import Iterable

from rag_knowledge_base.domain.models import Chunk, Document

_WORD_RE = re.compile(r"\w+", re.UNICODE)


def split_words(text: str) -> list[str]:
    return _WORD_RE.findall(text)


def chunk_documents(
    documents: Iterable[Document],
    *,
    max_words: int = 80,
    overlap_words: int = 16,
) -> list[Chunk]:
    if max_words <= 0:
        raise ValueError("max_words must be positive")
    if overlap_words < 0 or overlap_words >= max_words:
        raise ValueError("overlap_words must be >= 0 and lower than max_words")

    chunks: list[Chunk] = []
    for document in documents:
        words = split_words(document.text)
        if not words:
            continue
        start = 0
        chunk_number = 0
        while start < len(words):
            end = min(start + max_words, len(words))
            chunk_text = " ".join(words[start:end])
            chunks.append(
                Chunk(
                    id=f"{document.id}:{chunk_number}",
                    document_id=document.id,
                    title=document.title,
                    text=chunk_text,
                    metadata={**document.metadata, "chunk_number": str(chunk_number)},
                )
            )
            if end == len(words):
                break
            start = end - overlap_words
            chunk_number += 1
    return chunks
