# rag-knowledge-base Specification

## Purpose

Provide a local-first retrieval component whose architecture, filesystem boundary, and Recall@k evidence are reproducible.

## ADDED Requirements

### Requirement: correct Recall@k

The system SHALL compute each query's Recall@k as relevant documents recovered in the top k divided by all relevant documents for that query.

#### Scenario: partial recovery

- GIVEN a query has two relevant documents
- WHEN one relevant document appears in the top k
- THEN Recall@k is 0.5, not 1.0

### Requirement: replaceable integrations

Application code SHALL depend on embedding and vector-store ports. Concrete local adapters SHALL be selected outside the application boundary.

#### Scenario: adapter substitution

- GIVEN a compatible embedding provider and vector-store factory
- WHEN they are injected into `RetrievalService`
- THEN indexing, retrieval, and evaluation run without changing application code

### Requirement: confined HTTP filesystem access

FastAPI callers SHALL provide relative paths resolved below configured data or result roots.

#### Scenario: traversal attempt

- GIVEN an absolute path or a path containing `..`
- WHEN it is sent to ingest, query, or evaluate
- THEN the API returns HTTP 400 before filesystem access

### Requirement: honest benchmark repetitions

The benchmark SHALL distinguish repetitions, warm-up queries, recall samples, and timed query samples.

#### Scenario: default evaluation

- GIVEN 7 questions and 5 repetitions
- WHEN the benchmark runs
- THEN it records 5 macro recall samples and 35 timed query measurements
- AND excludes the 7 warm-up queries from latency metrics
