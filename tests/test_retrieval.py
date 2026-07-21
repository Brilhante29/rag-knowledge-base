from __future__ import annotations

import inspect
import tempfile
import unittest
from pathlib import Path

from rag_knowledge_base.application import use_cases
from rag_knowledge_base.application.use_cases import (
    DEFAULT_CORPUS,
    DEFAULT_QUESTIONS,
    RetrievalService,
    recall_at_k,
)
from rag_knowledge_base.infrastructure.composition import create_local_retrieval_service
from rag_knowledge_base.infrastructure.embeddings.hashing import HashingEmbeddingProvider
from rag_knowledge_base.infrastructure.stores.json_vector_store import JsonVectorStoreFactory


class RecordingStoreFactory:
    def __init__(self) -> None:
        self.delegate = JsonVectorStoreFactory()
        self.created = 0
        self.loaded = 0

    def create(self, dimension: int):
        self.created += 1
        return self.delegate.create(dimension)

    def load(self, path: Path):
        self.loaded += 1
        return self.delegate.load(path)


class RetrievalTests(unittest.TestCase):
    def test_query_returns_relevant_context(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            service = create_local_retrieval_service()
            index_path = Path(tmp) / "index.json"
            service.build_index(DEFAULT_CORPUS, index_path)
            response = service.answer(
                "How does vector search measure recall at k?",
                index_path=index_path,
                top_k=3,
            )
            document_ids = {context["document_id"] for context in response["contexts"]}
            self.assertIn("vector-search", document_ids)

    def test_recall_at_k_counts_every_relevant_document(self) -> None:
        self.assertEqual(recall_at_k({"one", "two"}, {"one", "other"}), 0.5)
        self.assertEqual(recall_at_k({"one", "two"}, {"one", "two", "other"}), 1.0)
        with self.assertRaisesRegex(ValueError, "at least one relevant"):
            recall_at_k(set(), {"one"})

    def test_service_uses_injected_store_factory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            factory = RecordingStoreFactory()
            service = RetrievalService(
                embedding_provider=HashingEmbeddingProvider(dimension=64),
                vector_stores=factory,
            )
            index_path = Path(tmp) / "index.json"
            service.build_index(DEFAULT_CORPUS, index_path)
            service.retrieve("vector search", index_path=index_path, top_k=1)

            self.assertEqual(factory.created, 1)
            self.assertEqual(factory.loaded, 1)
            self.assertNotIn("rag_knowledge_base.infrastructure", inspect.getsource(use_cases))

    def test_evaluation_records_honest_repetitions_and_recall(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            service = create_local_retrieval_service()
            index_path = Path(tmp) / "index.json"
            output_path = Path(tmp) / "result.json"
            result = service.evaluate_retrieval(
                DEFAULT_CORPUS,
                DEFAULT_QUESTIONS,
                index_path,
                output_path,
                top_k=3,
                repetitions=3,
            )

            self.assertGreaterEqual(result["summary"]["recall_at_k"], 0.85)
            self.assertEqual(result["summary"]["cost_per_query_usd"], 0.0)
            self.assertEqual(result["repeat"], 3)
            self.assertEqual(len(result["samples"]), 3)
            self.assertEqual(result["summary"]["timed_query_samples"], 21.0)
            self.assertEqual(len(result["measurements"]), 21)
            self.assertTrue(output_path.exists())

            q2 = [sample for sample in result["measurements"] if sample["question_id"] == "q2"]
            self.assertEqual(len(q2), 3)
            for sample in q2:
                expected = (
                    sample["recovered_relevant_documents"] / sample["relevant_documents"]
                )
                self.assertEqual(sample["recall_at_k"], expected)


if __name__ == "__main__":
    unittest.main()
