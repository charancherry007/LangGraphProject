# Task 1 — Knowledge Database Enhancement, JSON Ingestion & LLaMA Agent Wrappers

## Mission

Enhance the **existing AI Case Processing Platform** without disturbing, rewriting, or regressing working functionality.

This task covers:

1. Analyze the existing repository before making changes.
2. Reuse existing code blocks, functions, classes, interfaces, configuration, database clients, MCP tooling, LangGraph nodes, and tests wherever possible.
3. Convert the provided JSON knowledge base into Neo4j, PostgreSQL, and PostgreSQL/PGvector representations.
4. Create/enhance database wrapper/repository classes and a unified knowledge retrieval layer.
5. Implement/enhance agent wrappers using **LLaMA**.
6. Preserve the existing MCP tooling architecture and LangGraph pipeline.
7. Keep the implementation friendly to **GPT-6 Astra as the coding/implementation agent**: Astra must inspect first, reuse existing code, then make the smallest safe changes.

> **Important:** LLaMA is the runtime AI model required for this task's agent wrappers. GPT-6 Astra is the coding/engineering agent implementing the task. Do not replace the requested LLaMA runtime integration with GPT-6 Astra.

---

## 1. Analyze First — Never Start Coding Blindly

Before modifying any file, inspect the complete repository.

Review at minimum:

- repository tree
- README
- pyproject.toml / requirements
- `.env.example`
- config/settings
- existing database clients
- Neo4j implementation
- PostgreSQL implementation
- pgvector implementation
- embedding implementation
- existing AI/model abstraction
- existing LLaMA/GPT integration
- LangGraph graph/state/router
- existing agents
- MCP client and adapters
- services
- gateway
- tests

Search for reusable symbols such as:

```text
Neo4j
Postgres
pgvector
embedding
vector
LangGraph
StateGraph
MCP
agent
model
LLaMA
llama
knowledge
repository
checkpoint
```

If an existing function/class can be extended, extend it instead of creating a duplicate.

Create/update `docs/implementation_analysis.md` only if an appropriate analysis/design document does not already exist. Record:

```text
Existing Component
Location
Purpose
Reusable Functions/Classes
Required Extension
Reason for Change
What Will NOT Change
```

---

## 2. Reuse-First Engineering Rule

Follow this order:

```text
DISCOVER → UNDERSTAND → REUSE → EXTEND → TEST → CREATE NEW CODE ONLY IF NECESSARY
```

Do not create duplicate:

```text
model clients
DB clients
repositories
MCP clients
agents
LangGraph graphs
configuration systems
```

unless the analysis proves that a new abstraction is necessary.

---

## 3. Preserve Existing Architecture

Keep the existing dependency direction:

```text
Gateway
   ↓
Orchestration / LangGraph
   ↓
Agents
   ↓
Services / MCP
   ↓
Knowledge Layer
```

Extend the knowledge flow to:

```text
JSON Knowledge Base
        ↓
Canonical Knowledge Models
        ↓
Validation / Normalization
        ↓
 ┌──────┼────────┐
 ▼      ▼        ▼
Neo4j Postgres PGvector
 └──────┼────────┘
        ▼
Knowledge Retrieval Wrappers
        ↓
Existing Agent / LangGraph Pipeline
```

Do not create a parallel application architecture.

---

## 4. JSON Knowledge Base Analysis

Locate and inspect the provided JSON knowledge base using its **actual schema**.

Identify:

- case types
- markets
- LOBs
- channels
- CRDs
- CRD fields
- mandatory/optional fields
- documents
- validation rules
- relationships
- descriptions
- examples
- aliases/synonyms
- versions/metadata

Do not invent entities or relationships that are absent from the source.

If multiple JSON files exist, determine whether they are versions, domains, supplements, or independent sources and document the decision.

---

## 5. Canonical Knowledge Model

Create or reuse typed models between the JSON and target databases:

```text
JSON → Loader → Parser → Canonical Models → Neo4j/Postgres/PGvector
```

Reuse existing Pydantic/domain models where available.

Possible concepts include:

```text
KnowledgeBase
CaseType
Market
LOB
Channel
CRD
CRDField
DocumentRequirement
ValidationRule
KnowledgeExample
KnowledgeRelationship
```

Only implement concepts actually required by the source.

---

## 6. Knowledge Ingestion Pipeline

Implement or extend the existing ingestion pipeline:

```text
Load
 ↓
Parse
 ↓
Validate
 ↓
Normalize
 ↓
Deduplicate
 ↓
Generate Stable IDs
 ↓
Version
 ↓
Persist
```

Support, where compatible with existing CLI conventions:

```text
--validate-only
--dry-run
--force
```

The ingestion must be repeatable and safe.

---

## 7. Stable IDs and Versioning

Use deterministic identifiers based on stable business/source keys. Do not generate new random IDs on every ingestion.

Track:

```text
knowledge_version
source_file
source_hash
ingested_at
```

Avoid unnecessary full rebuilds when the source has not changed.

---

## 8. Neo4j Conversion

Convert the actual knowledge model into a meaningful graph.

Potential nodes:

```text
Market
LOB
Channel
CaseType
CRD
CRDField
Document
ValidationRule
Example
```

Potential relationships, only where supported by the source:

```text
HAS_LOB
HAS_CHANNEL
SUPPORTS_CASE_TYPE
REQUIRES_CRD
HAS_FIELD
REQUIRES_DOCUMENT
VALIDATED_BY
HAS_EXAMPLE
RELATED_TO
```

Requirements:

- idempotent writes
- `MERGE`/safe upsert where appropriate
- uniqueness constraints/indexes for stable IDs
- efficient lookup by case type, market, LOB, channel where applicable

Do not create meaningless relationships.

---

## 9. PostgreSQL Conversion

Reuse the existing PostgreSQL engine/session infrastructure.

Persist normalized knowledge using appropriate relational models. Possible concepts:

```text
knowledge_case_types
knowledge_markets
knowledge_lobs
knowledge_channels
knowledge_crds
knowledge_crd_fields
knowledge_documents
knowledge_validation_rules
knowledge_examples
knowledge_relationships
```

Adapt to the actual JSON schema.

Preserve existing operational/case tables. Do not overwrite unrelated application data.

Use appropriate:

- primary keys
- foreign keys
- unique constraints
- indexes
- source/version metadata
- timestamps

---

## 10. PGvector Conversion

Reuse the existing pgvector and embedding implementation.

Generate embeddings for meaningful semantic content such as:

```text
case type descriptions
CRD descriptions
field descriptions
document descriptions
validation rules
knowledge examples
aliases
```

Do not embed meaningless metadata.

Store traceable metadata:

```text
knowledge_id
entity_type
case_type
market
lob
channel
knowledge_version
source
```

Keep the embedding provider/model configurable.

---

## 11. Database Wrapper Classes

Create or extend wrappers so agents do not know database implementation details.

Preferred flow:

```text
Agent
 ↓
KnowledgeRetrievalService
 ↓
Repository / Wrapper
 ├── Neo4j
 ├── PostgreSQL
 └── PGvector
```

Expose operations such as:

```python
get_case_types(...)
get_case_type(...)
get_case_requirements(...)
get_crd_definition(...)
get_required_fields(...)
get_required_documents(...)
get_validation_rules(...)
search_knowledge(...)
search_historical_cases(...)
```

Reuse existing wrappers whenever possible.

---

## 12. Unified Knowledge Retrieval Service

Create or extend `KnowledgeRetrievalService`.

Responsibilities:

- structured graph lookup
- PostgreSQL lookup
- semantic vector retrieval
- result merging
- deduplication
- ranking
- source attribution
- knowledge version awareness

Agents should not directly execute Cypher, SQL, or vector SQL unless the existing architecture explicitly requires it.

---

## 13. LLaMA Runtime Integration

**Task 1 agent runtime must use LLaMA.**

First inspect the existing model abstraction.

If LLaMA is already supported, reuse it.

If multiple providers are already supported, extend the existing provider interface.

Only create a new provider if no suitable abstraction exists.

Possible configuration values:

```text
LLAMA_MODEL
LLAMA_API_KEY
LLAMA_BASE_URL
LLAMA_TIMEOUT
LLAMA_MAX_RETRIES
LLAMA_TEMPERATURE
```

Follow the project's existing naming conventions. Never hard-code credentials/endpoints.

---

## 14. LLaMA Agent Wrapper

Create or enhance a reusable wrapper such as `LlamaAgentWrapper`, or extend the existing agent/model interface.

Flow:

```text
Input
 ↓
Context Assembly
 ↓
LLaMA Invocation
 ↓
Structured Output
 ↓
Validation
 ↓
Agent Result
```

Support:

- timeout
- retry
- structured output
- error handling
- correlation ID
- case ID
- model metadata
- safe logging

Do not log sensitive prompts or complete customer payloads.

---

## 15. Classification Agent Wrapper

Extend the existing classifier instead of replacing it.

Inputs:

```text
incoming inquiry
structured knowledge candidates
vector semantic candidates
known metadata
```

Structured result should contain, as applicable:

```text
case_type
market
lob
channel
confidence
evidence
```

Selected taxonomy values must come from retrieved knowledge. LLaMA must not invent arbitrary case types.

---

## 16. MCP Architecture

Preserve the existing pattern:

```text
Agent
 ↓
MCP Adapter
 ↓
Shared MCP Client
 ↓
MCP Server
```

Reuse existing adapters for:

```text
CLIC
Griffin
Merchant
Consumer
Document Processing
```

Do not bypass the MCP adapter layer.

---

## 17. LangGraph Integration

Inspect the existing graph before editing.

Extend the current graph rather than creating a new graph.

Target concept:

```text
START
 ↓
Existing Normalization
 ↓
Knowledge Candidate Retrieval
 ↓
Existing/Enhanced Classifier
 ↓
Requirement Retrieval
 ↓
Existing/Enhanced Enrichment
 ↓
Gap Analysis
 ↓
Existing Router
 ↓
Update / Communication
 ↓
END
```

Preserve existing nodes, state fields, routes, and public behavior.

---

## 18. Error Handling

Reuse the existing exception architecture.

Handle safely:

```text
JSON validation
Neo4j
PostgreSQL
PGvector
embedding
LLaMA timeout/retry/malformed output
MCP
knowledge retrieval
```

Never silently turn an integration failure into successful classification or enrichment.

---

## 19. Ingestion Safety

Knowledge ingestion must:

- validate before writes
- use transactions where practical
- rollback on transactional failure
- use idempotent writes
- report rejected records
- avoid destructive operations by default

Provide an ingestion summary including source/version, processed/rejected records, database writes, embeddings, duration, and errors.

---

## 20. Tests

Run existing tests before changes and establish a baseline.

Add tests for:

### Ingestion

```text
loader
parser
validation
stable IDs
deduplication
Neo4j transformation
Postgres transformation
vector document generation
```

### Wrappers

```text
case type lookup
requirements lookup
CRD lookup
document lookup
semantic search
```

### LLaMA

Mock LLaMA and test:

```text
valid structured output
invalid output
timeout
retry
low confidence
model failure
```

All existing regression tests must continue to pass.

---

## 21. Acceptance Criteria

- [ ] Existing repository analyzed before modifications.
- [ ] Existing reusable functions/classes identified and reused.
- [ ] Existing functionality remains intact.
- [ ] Actual JSON KB schema is supported.
- [ ] Canonical knowledge models exist/reused.
- [ ] Neo4j ingestion works.
- [ ] PostgreSQL ingestion works.
- [ ] PGvector ingestion works.
- [ ] Stable IDs and knowledge versioning exist.
- [ ] Database wrappers exist/reuse existing wrappers.
- [ ] Unified knowledge retrieval exists.
- [ ] LLaMA runtime integration works through the existing model abstraction.
- [ ] Agent wrappers use LLaMA.
- [ ] MCP architecture remains intact.
- [ ] Existing LangGraph is extended, not duplicated.
- [ ] Ingestion is idempotent.
- [ ] Validation/dry-run exists.
- [ ] New tests pass.
- [ ] Existing regression tests pass.
- [ ] Documentation/configuration are updated without deleting useful content.

---

## 22. Final Engineering Rule

GPT-6 Astra must behave as an **existing-codebase engineer**, not a greenfield generator.

Before writing code:

```text
Search → Inspect → Understand → Reuse
```

Before replacing code:

```text
Prove replacement is necessary.
```

Before creating a new abstraction:

```text
Search for an existing abstraction first.
```

The final result must be an incremental, tested enhancement of the current platform, with **LLaMA as the runtime model for Task 1 agents**.
