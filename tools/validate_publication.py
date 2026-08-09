from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
V1_PATH = ROOT / "benchmarks" / "results" / "retrieval-baseline.json"
V2_PATH = ROOT / "benchmarks" / "publication" / "retrieval-baseline-v2.json"
SCHEMA_PATH = ROOT / ".portfolio" / "contracts" / "benchmark-result-v2.schema.json"
LOCK_PATH = ROOT / "requirements.lock"
VALIDATION_LOCK_PATH = ROOT / "requirements-validation.lock"
FIXTURE_PATHS = ["data/fixtures/corpus.jsonl", "data/fixtures/questions.jsonl"]


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain an object")
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256_bytes(value: bytes) -> str:
    return f"sha256:{hashlib.sha256(value).hexdigest()}"


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def git_bytes(commit: str, relative_path: str) -> bytes:
    completed = subprocess.run(
        [
            "git",
            "-c",
            f"safe.directory={ROOT}",
            "-C",
            str(ROOT),
            "show",
            f"{commit}:{relative_path}",
        ],
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise AssertionError(f"cannot read {relative_path} from source commit {commit}")
    return completed.stdout


def git_has_commit(commit: str) -> bool:
    completed = subprocess.run(
        [
            "git",
            "-c",
            f"safe.directory={ROOT}",
            "-C",
            str(ROOT),
            "cat-file",
            "-e",
            f"{commit}^{{commit}}",
        ],
        capture_output=True,
        check=False,
    )
    return completed.returncode == 0


def committed_fixture_digest(commit: str) -> str:
    digest = hashlib.sha256()
    for relative_path in FIXTURE_PATHS:
        digest.update(relative_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(git_bytes(commit, relative_path))
        digest.update(b"\0")
    return f"sha256:{digest.hexdigest()}"


def config_digest(v1: dict[str, Any]) -> str:
    summary = v1["summary"]
    config = {
        "benchmark_id": "rag-retrieval",
        "top_k": int(summary["top_k"]),
        "repetitions": int(v1["repeat"]),
        "warmup_queries": int(summary["warmup_queries"]),
        "concurrency": 1,
    }
    encoded = json.dumps(config, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(encoded)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-git", action="store_true")
    args = parser.parse_args()

    validation_lock = VALIDATION_LOCK_PATH.read_text(encoding="utf-8")
    require("jsonschema==4.26.0" in validation_lock, "jsonschema is not pinned")
    require("setuptools==80.9.0" in validation_lock, "setuptools is not pinned")

    import jsonschema

    v1 = read_json(V1_PATH)
    v2 = read_json(V2_PATH)
    schema = read_json(SCHEMA_PATH)
    jsonschema.Draft202012Validator(
        schema, format_checker=jsonschema.FormatChecker()
    ).validate(v2)

    require(v1.get("project") == "rag-knowledge-base", "unexpected V1 project")
    require(v2.get("project") == "rag-knowledge-base", "unexpected V2 project")
    require(v2.get("benchmark_id") == "rag-retrieval", "unexpected benchmark id")
    require(v1.get("metric") == "recall_at_3", "unexpected primary metric")
    require(v1.get("value") == 1.0, "unexpected Recall@3 baseline")
    require(v1.get("repeat") == 5, "unexpected repetition count")
    require(v1.get("samples") == [1.0] * 5, "unexpected Recall@3 samples")
    require(len(v1.get("latency_samples_ms", [])) == 35, "expected 35 latency samples")
    require(len(v1.get("measurements", [])) == 35, "expected 35 measurements")

    summary = v1.get("summary", {})
    require(summary.get("queries") == 7.0, "expected seven questions")
    require(summary.get("repetitions") == 5.0, "summary repetition mismatch")
    require(summary.get("timed_query_samples") == 35, "timed sample mismatch")
    require(summary.get("warmup_queries") == 7, "warmup count mismatch")
    require(summary.get("cost_per_query_usd") == 0.0, "offline cost mismatch")

    metrics = {metric["name"]: metric for metric in v2["metrics"]}
    require(set(metrics) == {"recall_at_3", "p95_latency_ms", "cost_per_query_usd"}, "unexpected V2 metrics")
    require(metrics["recall_at_3"]["value"] == v1["value"], "Recall V1/V2 mismatch")
    require(metrics["recall_at_3"]["samples"] == v1["samples"], "Recall samples mismatch")
    require(metrics["p95_latency_ms"]["value"] == summary["p95_latency_ms"], "p95 V1/V2 mismatch")
    require(metrics["p95_latency_ms"]["samples"] == v1["latency_samples_ms"], "latency samples mismatch")
    require(metrics["cost_per_query_usd"]["value"] == 0.0, "unexpected V2 cost")
    require(all(metric["failures"] == 0 for metric in metrics.values()), "publication contains failures")
    require(v2["execution"]["repeat"] == 5, "execution repeat mismatch")
    require(v2["workload"]["measured_iterations"] == 5, "workload repetition mismatch")
    require(v2["workload"]["warmup_iterations"] == 7, "workload warmup mismatch")
    require(v2["workload"]["concurrency"] == 1, "workload concurrency mismatch")
    require(v2["workload"]["config_digest"] == config_digest(v1), "config digest mismatch")
    require(v2["provenance"]["artifact_digest"] == sha256_file(V1_PATH), "raw artifact digest mismatch")
    require(
        re.fullmatch(r"sha256:[0-9a-f]{64}", v2["provenance"]["image_digest"])
        is not None,
        "invalid image digest",
    )

    manifest = (ROOT / "project.yaml").read_text(encoding="utf-8")
    require(re.search(r"(?m)^status:\s*published\s*$", manifest) is not None, "project is not published")
    require(
        "result_path: benchmarks/publication/retrieval-baseline-v2.json" in manifest,
        "manifest V2 path mismatch",
    )
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for expected in ("Recall@3 = `1.00`", f"{summary['p95_latency_ms']:.4f}", "35 timed query samples"):
        require(expected in readme, f"README is missing benchmark evidence {expected}")

    source_commit = v2["provenance"]["source_commit"]
    if args.require_git:
        require(git_has_commit(source_commit), "source commit unavailable; fetch full history")
        require(
            v2["workload"]["fixture_digest"] == committed_fixture_digest(source_commit),
            "committed fixture digest mismatch",
        )
        require(
            v2["provenance"]["dependency_lock_digest"]
            == sha256_bytes(git_bytes(source_commit, "requirements.lock")),
            "committed dependency lock digest mismatch",
        )

    serialized = json.dumps({"v1": v1, "v2": v2})
    for forbidden in ("C:\\Users\\", "github" + "_pat_", "gh" + "p_"):
        require(forbidden not in serialized, f"forbidden value in evidence: {forbidden}")
    print("publication_evidence=passed")


if __name__ == "__main__":
    main()