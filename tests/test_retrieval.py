from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from rag_knowledge_base.application.use_cases import (
    DEFAULT_CORPUS,
    DEFAULT_QUESTIONS,
    answer,
    build_index,
    evaluate_retrieval,
)


class RetrievalTests(unittest.TestCase):
    def test_query_returns_relevant_context(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            index_path = Path(tmp) / "index.json"
            build_index(DEFAULT_CORPUS, index_path)
            response = answer("How does vector search measure recall at k?", index_path=index_path, top_k=3)
            document_ids = {context["document_id"] for context in response["contexts"]}
            self.assertIn("vector-search", document_ids)

    def test_evaluation_reaches_expected_recall(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            index_path = Path(tmp) / "index.json"
            output_path = Path(tmp) / "result.json"
            result = evaluate_retrieval(
                DEFAULT_CORPUS,
                DEFAULT_QUESTIONS,
                index_path,
                output_path,
                top_k=3,
            )
            self.assertGreaterEqual(result["summary"]["recall_at_k"], 0.85)
            self.assertEqual(result["summary"]["cost_per_query_usd"], 0.0)
            self.assertTrue(output_path.exists())


if __name__ == "__main__":
    unittest.main()
