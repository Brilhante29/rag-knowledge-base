from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from rag_knowledge_base.application.use_cases import (
    DEFAULT_CORPUS,
    DEFAULT_INDEX,
    DEFAULT_QUESTIONS,
    DEFAULT_RESULT,
    answer,
    build_index,
    evaluate_retrieval,
)


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="rag-kb")
    subcommands = parser.add_subparsers(dest="command", required=True)

    ingest = subcommands.add_parser("ingest")
    ingest.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    ingest.add_argument("--index", type=Path, default=DEFAULT_INDEX)

    query = subcommands.add_parser("query")
    query.add_argument("question")
    query.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    query.add_argument("--top-k", type=int, default=3)

    evaluate = subcommands.add_parser("evaluate")
    evaluate.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    evaluate.add_argument("--questions", type=Path, default=DEFAULT_QUESTIONS)
    evaluate.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    evaluate.add_argument("--output", type=Path, default=DEFAULT_RESULT)
    evaluate.add_argument("--top-k", type=int, default=3)

    serve = subcommands.add_parser("serve")
    serve.add_argument("--host", default="0.0.0.0")
    serve.add_argument("--port", type=int, default=8000)

    args = parser.parse_args(argv)

    if args.command == "ingest":
        print(json.dumps(build_index(args.corpus, args.index), indent=2))
    elif args.command == "query":
        print(json.dumps(answer(args.question, index_path=args.index, top_k=args.top_k), indent=2))
    elif args.command == "evaluate":
        print(
            json.dumps(
                evaluate_retrieval(
                    args.corpus,
                    args.questions,
                    args.index,
                    args.output,
                    top_k=args.top_k,
                ),
                indent=2,
            )
        )
    elif args.command == "serve":
        import uvicorn

        uvicorn.run("rag_knowledge_base.interfaces.api:app", host=args.host, port=args.port)
