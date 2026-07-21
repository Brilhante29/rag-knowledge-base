from __future__ import annotations

from rag_knowledge_base.application.use_cases import RetrievalService
from rag_knowledge_base.infrastructure.embeddings.hashing import HashingEmbeddingProvider
from rag_knowledge_base.infrastructure.stores.json_vector_store import JsonVectorStoreFactory


def create_local_retrieval_service(*, dimension: int = 384) -> RetrievalService:
    return RetrievalService(
        embedding_provider=HashingEmbeddingProvider(dimension=dimension),
        vector_stores=JsonVectorStoreFactory(),
    )
