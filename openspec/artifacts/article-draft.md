# #3 rag-knowledge-base: Recall@3 = 1.00

The corrected Docker baseline runs five complete repetitions over seven questions: Recall@3 is 1.00, average query latency is 1.65 ms, p95 is 1.97 ms, and paid API cost is zero.

The important part is what the number now means. Recall is computed per question as relevant documents recovered divided by all relevant documents. One fixture question has two relevant documents, so partial recovery would score 0.5 instead of being promoted to a full hit. The result stores five macro recall samples, 35 timed query measurements, and excludes seven warm-ups.

The architecture claim is enforced too. `RetrievalService` receives embedding and vector-store ports; concrete hashing/JSON adapters are selected in an infrastructure composition root. FastAPI callers can use only relative paths below configured data and result roots, while the trusted local CLI retains explicit path control.

This remains a small deterministic fixture. It proves the local retrieval pipeline, benchmark semantics, and replaceable boundary. It does not claim production retrieval quality. The next useful comparison is a model-backed embedding adapter on a harder dataset using the same measurement contract.
