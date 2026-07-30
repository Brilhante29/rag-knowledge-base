"""Produce the publication benchmark contract from a clean Docker run."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path


def sha256_bytes(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def combined_digest(root: Path, paths: list[str]) -> str:
    digest = hashlib.sha256()
    for relative in paths:
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update((root / relative).read_bytes())
        digest.update(b"\0")
    return "sha256:" + digest.hexdigest()


def git_output(root: Path, *arguments: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *arguments], text=True).strip()


def run_docker(root: Path, image: str, output_path: Path, repetitions: int) -> None:
    result_dir = output_path.parent.resolve()
    command = [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{result_dir}:/results",
        "--entrypoint",
        "python",
        image,
        "-m",
        "rag_knowledge_base",
        "evaluate",
        "--repetitions",
        str(repetitions),
        "--output",
        f"/results/{output_path.name}",
    ]
    subprocess.run(command, cwd=root, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", default="rag-knowledge-base:benchmark")
    parser.add_argument("--repetitions", type=int, default=5)
    parser.add_argument(
        "--producer", choices=("local", "github-actions", "other-ci"), default="local"
    )
    parser.add_argument("--ci-run-url", default=None)
    parser.add_argument(
        "--output",
        default="benchmarks/publication/retrieval-baseline-v2.json",
    )
    parser.add_argument("--skip-build", action="store_true")
    args = parser.parse_args()

    if args.repetitions < 2:
        raise SystemExit("--repetitions must be at least 2")
    if args.producer != "local" and not args.ci_run_url:
        raise SystemExit("--ci-run-url is required for a non-local producer")

    root = Path(__file__).resolve().parents[1]
    source_commit = git_output(root, "rev-parse", "HEAD")
    if git_output(root, "status", "--porcelain"):
        raise SystemExit("benchmark requires a clean tree before it starts")

    output_path = root / args.output
    v1_path = root / "benchmarks/results/retrieval-baseline.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not args.skip_build:
        subprocess.run(["docker", "build", "-t", args.image, str(root)], cwd=root, check=True)

    image_id = subprocess.check_output(
        ["docker", "image", "inspect", "--format", "{{.Id}}", args.image],
        text=True,
    ).strip()
    if not image_id.startswith("sha256:"):
        raise SystemExit(f"unexpected Docker image id: {image_id}")

    started_at = datetime.now(timezone.utc)
    started = time.perf_counter()
    run_docker(root, args.image, v1_path, args.repetitions)
    duration = time.perf_counter() - started

    result = json.loads(v1_path.read_text(encoding="utf-8"))
    summary = result["summary"]
    latency_samples = [float(value) for value in result["latency_samples_ms"]]
    image_ref = f"{args.image}@{image_id}"
    config = {
        "benchmark_id": "rag-retrieval",
        "top_k": int(summary["top_k"]),
        "repetitions": int(result["repeat"]),
        "warmup_queries": int(summary["warmup_queries"]),
        "concurrency": 1,
    }

    metrics = [
        {
            "name": "recall_at_3",
            "value": float(result["value"]),
            "unit": "ratio",
            "direction": "higher_is_better",
            "samples": [float(value) for value in result["samples"]],
            "failures": 0,
            "summary": {"macro_recall_at_k": float(summary["recall_at_k"])},
        },
        {
            "name": "p95_latency_ms",
            "value": float(summary["p95_latency_ms"]),
            "unit": "ms",
            "direction": "lower_is_better",
            "samples": latency_samples,
            "failures": 0,
            "summary": {
                "avg_latency_ms": float(summary["avg_latency_ms"]),
                "p95_latency_ms": float(summary["p95_latency_ms"]),
            },
        },
        {
            "name": "cost_per_query_usd",
            "value": float(summary["cost_per_query_usd"]),
            "unit": "USD/query",
            "direction": "lower_is_better",
            "samples": [float(summary["cost_per_query_usd"])],
            "failures": 0,
            "summary": {"offline": True},
        },
    ]

    publication = {
        "schema_version": 2,
        "run_id": str(uuid.uuid4()),
        "project": "rag-knowledge-base",
        "benchmark_id": "rag-retrieval",
        "workload": {
            "version": "1.0.0",
            "fixture_digest": combined_digest(
                root, ["data/fixtures/corpus.jsonl", "data/fixtures/questions.jsonl"]
            ),
            "config_digest": sha256_bytes(
                json.dumps(config, sort_keys=True, separators=(",", ":")).encode("utf-8")
            ),
            "warmup_iterations": int(summary["warmup_queries"]),
            "measured_iterations": int(result["repeat"]),
            "concurrency": 1,
        },
        "metrics": metrics,
        "execution": {
            "command": (
                f"docker run --rm --entrypoint python {args.image} "
                f"-m rag_knowledge_base evaluate --repetitions {args.repetitions}"
            ),
            "started_at": started_at.isoformat().replace("+00:00", "Z"),
            "duration_seconds": round(duration, 6),
            "exit_code": 0,
            "repeat": int(args.repetitions),
        },
        "environment": {
            "runtime": "python-3.12-slim",
            "architecture": platform.machine().lower(),
            "hardware_class": "docker-local" if args.producer == "local" else "github-actions-ubuntu-latest",
        },
        "provenance": {
            "source_commit": source_commit,
            "clean_tree": True,
            "image_ref": image_ref,
            "image_digest": image_id,
            "dependency_lock_digest": sha256_file(root / "requirements.lock"),
            "producer": args.producer,
            "artifact_digest": sha256_file(v1_path),
        },
        "comparability_key": "rag-retrieval:1.0.0:hashing-384:json-vector-store:x86_64",
    }
    if args.ci_run_url:
        publication["provenance"]["ci_run_url"] = args.ci_run_url

    output_path.write_text(json.dumps(publication, indent=2) + "\n", encoding="utf-8")
    print(f"v2_result={output_path}")
    print(f"source_commit={source_commit}")
    print(f"image_digest={image_id}")
    print(f"artifact_digest={publication['provenance']['artifact_digest']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
