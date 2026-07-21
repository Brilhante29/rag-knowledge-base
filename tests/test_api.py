from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from rag_knowledge_base.interfaces.api import ApiPathPolicy, create_app

ROOT = Path(__file__).resolve().parents[1]


class ApiPathSecurityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        root = Path(self.temp_dir.name)
        self.data_root = root / "data"
        self.result_root = root / "results"
        fixture_root = self.data_root / "fixtures"
        fixture_root.mkdir(parents=True)
        self.result_root.mkdir(parents=True)
        shutil.copyfile(ROOT / "data/fixtures/corpus.jsonl", fixture_root / "corpus.jsonl")
        shutil.copyfile(
            ROOT / "data/fixtures/questions.jsonl",
            fixture_root / "questions.jsonl",
        )
        self.client = TestClient(
            create_app(
                path_policy=ApiPathPolicy(
                    data_root=self.data_root,
                    result_root=self.result_root,
                )
            )
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_default_api_flow_stays_inside_configured_roots(self) -> None:
        ingest = self.client.post("/ingest", json={})
        self.assertEqual(ingest.status_code, 200, ingest.text)
        self.assertTrue((self.data_root / "runtime/index.json").exists())

        query = self.client.post("/query", json={"question": "What is vector search?"})
        self.assertEqual(query.status_code, 200, query.text)

        evaluation = self.client.post("/evaluate", json={"repetitions": 2})
        self.assertEqual(evaluation.status_code, 200, evaluation.text)
        self.assertEqual(evaluation.json()["repeat"], 2)
        self.assertTrue((self.result_root / "retrieval-baseline.json").exists())

    def test_rejects_traversal_and_absolute_paths(self) -> None:
        cases = [
            ("/ingest", {"corpus_path": "../secrets.txt"}),
            ("/query", {"question": "test", "index_path": "C:\\secrets.json"}),
            ("/evaluate", {"output_path": "../outside.json"}),
            ("/evaluate", {"questions_path": "/etc/passwd"}),
        ]
        for endpoint, payload in cases:
            with self.subTest(endpoint=endpoint, payload=payload):
                response = self.client.post(endpoint, json=payload)
                self.assertEqual(response.status_code, 400, response.text)


if __name__ == "__main__":
    unittest.main()
