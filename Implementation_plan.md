# Master Task — AI Case Processing Platform Architecture Setup

## 1. Objective

Set up a production-ready Python project skeleton for an AI-powered case processing platform using:

- FastAPI for API/event ingestion
- LangGraph for workflow orchestration
- Specialized AI agents for classification, enrichment, gap analysis, and communication
- MCP clients/adapters for external enterprise integrations
- Neo4j for graph-based knowledge and validation rules
- PostgreSQL + pgvector for relational state, audit data, historical cases, transcripts, and semantic retrieval
- Redis for optional transient state/cache
- Docker Compose for local infrastructure
- Pydantic Settings for configuration
- Pytest for unit and integration testing

The immediate goal is to create the complete repository architecture, configuration, infrastructure, interfaces, schemas, dependency wiring, health checks, test foundations, and documentation.

Do **not** implement complex domain-specific business logic yet. Create clean interfaces and minimal working implementations/stubs so the application can start, tests can run, and future agents/services can be implemented incrementally.

---

# 2. Target Repository Structure

Create the repository with the following structure:

```text
.
├── .env.example
├── .gitignore
├── README.md
├── pyproject.toml
├── docker-compose.yml
├── Dockerfile
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   └── logging_config.py
│
├── src/
│   ├── __init__.py
│   │
│   ├── gateway/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── normalizers.py
│   │   └── schemas.py
│   │
│   ├── orchestration/
│   │   ├── __init__.py
│   │   ├── graph.py
│   │   ├── state.py
│   │   ├── checkpointing.py
│   │   └── router.py
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── case_classify_agent.py
│   │   ├── enrichment_agent.py
│   │   ├── gap_analysis_agent.py
│   │   └── communication_agent.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── update_case_service.py
│   │
│   ├── mcp_tools/
│   │   ├── __init__.py
│   │   ├── client.py
│   │   ├── clic_mcp.py
│   │   ├── griffin_mcp.py
│   │   ├── merchant_mcp.py
│   │   ├── consumer_mcp.py
│   │   └── doc_processing_mcp.py
│   │
│   ├── knowledge/
│   │   ├── __init__.py
│   │   ├── neo4j/
│   │   │   ├── __init__.py
│   │   │   ├── client.py
│   │   │   └── queries.py
│   │   ├── vector_db/
│   │   │   ├── __init__.py
│   │   │   ├── client.py
│   │   │   └── embeddings.py
│   │   └── postgres/
│   │       ├── __init__.py
│   │       ├── client.py
│   │       └── models.py
│   │
│   └── utils/
│       ├── __init__.py
│       └── security.py
│
└── tests/
    ├── unit/
    │   ├── test_normalizers.py
    │   ├── test_agents.py
    │   └── test_mcp_tools.py
    └── integration/
        ├── test_orchestration_graph.py
        └── test_knowledge_retrieval.py
```

You may add small supporting modules such as:

```text
src/main.py
src/dependencies.py
src/exceptions.py
src/constants.py
```

if required for clean application wiring.

---

# 3. Implementation Principles

Follow these principles throughout the implementation:

1. Use Python 3.11+.
2. Prefer `pyproject.toml` over `requirements.txt`.
3. Use type hints throughout the codebase.
4. Use Pydantic v2 models for API/configuration contracts.
5. Use async APIs where appropriate.
6. Keep external integrations behind interfaces/adapters.
7. Do not hard-code credentials, URLs, API keys, database passwords, model names, or environment-specific values.
8. All configuration must come from environment variables.
9. Use dependency injection where practical.
10. Keep agents independent from infrastructure details.
11. Keep MCP adapters independent from LangGraph nodes.
12. Keep database access isolated in the knowledge layer.
13. Avoid circular imports.
14. Provide meaningful logging without logging secrets or sensitive payloads.
15. Make all external integrations mockable for unit tests.
16. Fail gracefully when optional external systems are unavailable.
17. Use structured errors/exceptions.
18. Do not silently swallow exceptions.
19. Add docstrings for public classes/functions.
20. Keep the initial implementation minimal but executable.

---

# 4. Phase 1 — Repository Scaffolding

## Tasks

- Create all directories listed above.
- Add `__init__.py` files where appropriate.
- Create `src/main.py`.
- Create `src/dependencies.py` if dependency wiring requires it.
- Create all requested modules.
- Ensure the repository can be imported without errors.

## Acceptance Criteria

```bash
python -m compileall src config
```

must succeed.

The project should have a clear separation between:

```text
Gateway
   ↓
Orchestration
   ↓
Agents
   ↓
Services / MCP / Knowledge
```

---

# 5. Phase 2 — Python Project Configuration

Create `pyproject.toml`.

Include appropriate dependencies for:

- FastAPI
- Uvicorn
- Pydantic
- Pydantic Settings
- LangGraph
- LangChain core/components required by the implementation
- PostgreSQL async driver
- SQLAlchemy
- pgvector
- Neo4j Python driver
- Redis
- HTTP client
- pytest
- pytest-asyncio
- httpx
- Ruff
- MyPy or an equivalent type checker

Do not add unnecessary dependencies.

Create useful development commands such as:

```bash
pytest
pytest -m integration
ruff check .
ruff format .
mypy src
uvicorn src.main:app --reload
```

If using an alternative dependency manager, document the commands in `README.md`.

---

# 6. Phase 3 — Environment Configuration

Create `.env.example`.

Include configuration categories for:

## Application

```text
APP_NAME
APP_ENV
APP_VERSION
LOG_LEVEL
DEBUG
```

## AI Models

```text
AI_PROVIDER
AI_MODEL
AI_API_KEY
AI_BASE_URL
```

The design must allow future support for multiple model providers.

## PostgreSQL

```text
POSTGRES_HOST
POSTGRES_PORT
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_URL
```

## pgvector

Include any configuration required by the selected vector implementation.

## Neo4j

```text
NEO4J_URI
NEO4J_USER
NEO4J_PASSWORD
NEO4J_DATABASE
```

## Redis

```text
REDIS_URL
```

## MCP

Provide endpoint configuration for:

```text
MCP_CLIC_URL
MCP_GRIFFIN_URL
MCP_MERCHANT_URL
MCP_CONSUMER_URL
MCP_DOC_PROCESSING_URL
MCP_TIMEOUT_SECONDS
MCP_RETRY_COUNT
```

## Security

Include placeholders for:

```text
API_AUTH_ENABLED
API_AUTH_TOKEN
```

Never commit real secrets.

---

# 7. Phase 4 — Pydantic Settings

Implement:

```text
config/settings.py
```

Create a strongly typed Pydantic Settings configuration object.

Requirements:

- Load values from `.env`.
- Provide sensible development defaults where safe.
- Validate required production configuration.
- Group configuration logically.
- Expose a reusable settings instance/function.
- Avoid reading environment variables throughout the application directly.

Example conceptual structure:

```python
class Settings(BaseSettings):
    app: AppSettings
    ai: AISettings
    postgres: PostgresSettings
    neo4j: Neo4jSettings
    redis: RedisSettings
    mcp: MCPSettings
    security: SecuritySettings
```

The exact implementation may differ if a flatter Pydantic Settings structure is cleaner.

---

# 8. Phase 5 — Logging

Implement:

```text
config/logging_config.py
```

Requirements:

- Centralized logging configuration.
- Configurable log level.
- Consistent log format.
- Include timestamp, logger name, level, and message.
- Support development-friendly logging.
- Do not log API keys, passwords, tokens, authentication headers, or full sensitive case payloads.

Add startup logging to the application.

---

# 9. Phase 6 — FastAPI Application

Create:

```text
src/main.py
```

Requirements:

- Initialize FastAPI.
- Register gateway routes.
- Initialize logging.
- Provide startup/shutdown lifecycle hooks.
- Initialize/release database and client resources cleanly.
- Provide a health endpoint.

Required endpoints:

```text
GET /health
GET /ready
```

Health should indicate that the process is alive.

Readiness should validate required dependencies where practical.

Add API metadata:

```text
title
description
version
```

---

# 10. Phase 7 — Gateway Layer

## `src/gateway/schemas.py`

Define normalized ingestion contracts.

Create a canonical event model such as:

```text
IngestionEvent
```

It should support:

- event ID
- source/channel
- timestamp
- case ID if known
- user/customer identifier if available
- payload
- metadata
- correlation ID
- idempotency key

Supported channels:

```text
PHONE
EMAIL
DOCUMENT
API
```

Create additional models if required.

## `src/gateway/normalizers.py`

Implement normalizers that transform raw channel payloads into the canonical `IngestionEvent`.

Provide functions/classes for:

```text
phone → normalized event
email → normalized event
document → normalized event
generic API → normalized event
```

Requirements:

- Validate input.
- Preserve relevant metadata.
- Generate correlation/idempotency information when missing.
- Do not embed business decisions inside normalizers.

## `src/gateway/routes.py`

Create endpoints such as:

```text
POST /events/phone
POST /events/email
POST /events/document
POST /events
```

Requirements:

- Validate payloads using Pydantic.
- Normalize incoming payloads.
- Return a tracking/correlation ID.
- Invoke the orchestration layer.
- Avoid putting orchestration logic directly into route handlers.

---

# 11. Phase 8 — LangGraph State

Implement:

```text
src/orchestration/state.py
```

Create a strongly typed case-processing state.

The state should be able to carry:

```text
case_id
correlation_id
channel
raw_input
normalized_event
case_type
classification_confidence
consumer_context
merchant_context
documents
transcript
retrieved_context
crd_data
missing_fields
validation_results
gap_questions
agent_results
communication_status
final_case_update
errors
status
audit_metadata
```

Use `TypedDict`, Pydantic models, or a combination where appropriate.

Ensure state is serializable for checkpointing.

---

# 12. Phase 9 — LangGraph Workflow

Implement:

```text
src/orchestration/graph.py
```

Create the main LangGraph `StateGraph`.

Initial conceptual flow:

```text
START
  ↓
Classify Case
  ↓
Route Based on Case Type
  ↓
Enrichment
  ↓
Gap Analysis
  ↓
Decision
  ├── Missing Information → Communication
  └── Complete → Update Case
  ↓
END
```

The implementation should keep nodes small and independently testable.

Do not hard-code complex business rules.

Expose a compiled graph/application object through a clean function.

---

# 13. Phase 10 — Graph Router

Implement:

```text
src/orchestration/router.py
```

Responsibilities:

- Determine consumer vs merchant routing.
- Determine whether additional enrichment is required.
- Determine whether gaps exist.
- Determine whether communication is required.
- Determine whether the case can proceed to final update.

Use explicit, testable functions.

Avoid embedding routing logic directly inside agent implementations.

---

# 14. Phase 11 — Checkpointing

Implement:

```text
src/orchestration/checkpointing.py
```

Requirements:

- Provide an abstraction for LangGraph checkpoint storage.
- Prefer PostgreSQL for durable workflow state.
- Allow Redis to be used for transient state where appropriate.
- Keep checkpoint implementation replaceable.
- Support correlation/thread IDs.
- Document local development behavior.

Do not tightly couple graph construction to one specific checkpointer implementation.

---

# 15. Phase 12 — Agent Base Interface

Implement:

```text
src/agents/base.py
```

Create a reusable agent abstraction.

It should support:

- agent name
- input state
- output state
- model/client dependency
- prompt/instruction
- structured result
- logging
- error handling

The base abstraction must not assume a specific AI provider.

Design for future support of:

```text
GPT
LLaMA
Other OpenAI-compatible models
```

---

# 16. Phase 13 — Case Classification Agent

Implement:

```text
src/agents/case_classify_agent.py
```

Responsibilities:

- Determine case category.
- Consumer vs merchant classification.
- Return confidence.
- Return reasoning metadata where appropriate.
- Produce structured output.

Expected conceptual output:

```text
case_type
confidence
classification
```

Keep the model call behind a replaceable interface.

Do not hard-code production prompts if business requirements are not yet finalized.

---

# 17. Phase 14 — Enrichment Agent

Implement:

```text
src/agents/enrichment_agent.py
```

Responsibilities:

- Consolidate incoming case information.
- Retrieve relevant context.
- Combine information from MCP systems.
- Retrieve historical/semantic context.
- Populate CRD-related data structures.

The agent should orchestrate tools rather than contain low-level database/network code.

---

# 18. Phase 15 — Gap Analysis Agent

Implement:

```text
src/agents/gap_analysis_agent.py
```

Responsibilities:

- Validate required information.
- Identify missing fields.
- Identify conflicting information.
- Determine additional questions required.
- Use graph knowledge/rules where appropriate.
- Return structured validation results.

Example output:

```text
is_complete
missing_fields
conflicts
questions
validation_results
```

---

# 19. Phase 16 — Communication Agent

Implement:

```text
src/agents/communication_agent.py
```

Responsibilities:

- Generate notification content.
- Prepare email/message payloads.
- Route communication to CM/CCP.
- Return communication status.

For the initial implementation, provide a mock/dry-run dispatcher.

Do not send real emails/messages unless an explicit integration is configured.

---

# 20. Phase 17 — Business Service Layer

Implement:

```text
src/services/update_case_service.py
```

Responsibilities:

- Apply final case changes.
- Persist case state.
- Update CRD-related information through appropriate MCP adapter.
- Record audit information.
- Ensure operations are idempotent where practical.

The service should not contain LLM-specific logic.

---

# 21. Phase 18 — MCP Client Infrastructure

Implement:

```text
src/mcp_tools/client.py
```

Create a reusable MCP client/session abstraction.

Requirements:

- Endpoint configuration.
- Connection/session lifecycle.
- Request timeout.
- Retry handling.
- Structured errors.
- Logging.
- Authentication hooks.
- Mockable interface for tests.

Avoid coupling business agents directly to HTTP/network details.

---

# 22. Phase 19 — CLIC MCP Adapter

Implement:

```text
src/mcp_tools/clic_mcp.py
```

Expose typed methods for conceptual operations:

```text
read_case()
update_crd()
create_case()
```

Use placeholder request/response models where actual contracts are unavailable.

Clearly document where real MCP schemas must be inserted.

---

# 23. Phase 20 — Griffin MCP Adapter

Implement:

```text
src/mcp_tools/griffin_mcp.py
```

Expose:

```text
fetch_griffin_link()
download_document()
```

Keep document retrieval separate from document processing.

---

# 24. Phase 21 — Merchant MCP Adapter

Implement:

```text
src/mcp_tools/merchant_mcp.py
```

Provide adapter methods for:

```text
RUMS
MSP
Genesis
```

Use typed interfaces.

Do not implement fake production behavior that could be mistaken for real integration.

---

# 25. Phase 22 — Consumer MCP Adapter

Implement:

```text
src/mcp_tools/consumer_mcp.py
```

Provide adapter methods for:

```text
C360
GAR
```

Keep integration details isolated.

---

# 26. Phase 23 — Document Processing MCP

Implement:

```text
src/mcp_tools/doc_processing_mcp.py
```

Provide methods for:

```text
OCR
IDP
PDF verification
```

Use structured request/response models.

---

# 27. Phase 24 — Neo4j Knowledge Layer

Implement:

```text
src/knowledge/neo4j/client.py
src/knowledge/neo4j/queries.py
```

Neo4j should represent knowledge such as:

```text
CRDs
validation rules
market specifications
case relationships
field dependencies
```

Requirements:

- Async/sync approach should be consistent with the application.
- Connection management must be centralized.
- Queries must be isolated in `queries.py`.
- Do not scatter Cypher queries throughout agents.
- Provide health-check functionality.
- Make the client mockable.

Add initial example query methods but do not invent detailed production domain rules.

---

# 28. Phase 25 — PostgreSQL Knowledge Layer

Implement:

```text
src/knowledge/postgres/client.py
src/knowledge/postgres/models.py
```

Use SQLAlchemy.

Provide initial models for:

```text
Case
CaseStatus
AuditEvent
CaseContext
```

At minimum support:

- case ID
- status
- timestamps
- correlation ID
- serialized context
- audit metadata

Add database session management.

Design the schema so migrations can be introduced later.

---

# 29. Phase 26 — pgvector Layer

Implement:

```text
src/knowledge/vector_db/client.py
src/knowledge/vector_db/embeddings.py
```

Use PostgreSQL + pgvector.

Support semantic retrieval for conceptual data such as:

```text
historical cases
transcripts
case notes
documents
```

Create abstractions for:

```text
generate_embedding()
store_embedding()
similarity_search()
```

Do not bind the implementation to one embedding provider.

The embedding dimension must be configurable or clearly isolated so it can be changed when the actual embedding model is selected.

---

# 30. Phase 27 — Redis

Configure Redis in Docker Compose.

Use Redis abstraction for:

- transient state
- caching
- optional event coordination

Do not make Redis mandatory for durable case state.

Durable state must remain recoverable from PostgreSQL/checkpoint storage.

---

# 31. Phase 28 — Security Utilities

Implement:

```text
src/utils/security.py
```

Provide reusable utilities for:

- token/API-key validation hooks
- secret masking
- safe logging
- request correlation IDs
- basic authorization dependency

The implementation can initially use a configurable static API token for local development.

Never expose secrets in logs.

---

# 32. Phase 29 — Docker Compose

Create:

```text
docker-compose.yml
```

Include:

### PostgreSQL

- persistent volume
- configured database/user/password
- pgvector-enabled image or initialization
- health check

### Neo4j

- persistent volume
- authentication
- HTTP/Bolt ports
- health check

### Redis

- persistent volume if useful
- port
- health check

### Application

Optionally include the FastAPI service.

The Compose configuration should allow:

```bash
docker compose up -d
```

to start the infrastructure.

Document connection URLs.

Do not expose production credentials.

---

# 33. Phase 30 — Dockerfile

Create a production-oriented Dockerfile.

Requirements:

- Python 3.11+
- non-root runtime user
- dependency installation
- application source copy
- environment configuration
- health check where appropriate
- run FastAPI using Uvicorn

Keep the image reasonably small.

---

# 34. Phase 31 — Unit Tests

Implement:

```text
tests/unit/test_normalizers.py
tests/unit/test_agents.py
tests/unit/test_mcp_tools.py
```

Tests should cover:

## Normalizers

- phone payload normalization
- email payload normalization
- document payload normalization
- missing required fields
- correlation ID generation
- idempotency handling

## Agents

- classification result parsing
- confidence validation
- enrichment state transformation
- gap detection
- communication result handling

Use mocked AI/model dependencies.

## MCP

- successful request
- timeout
- retry
- malformed response
- authentication failure
- connection failure

No real enterprise MCP endpoints should be required for unit tests.

---

# 35. Phase 32 — Integration Tests

Implement:

```text
tests/integration/test_orchestration_graph.py
tests/integration/test_knowledge_retrieval.py
```

## Graph Integration

Validate that:

```text
START → classification → enrichment → gap analysis → decision
```

executes correctly with mocked external integrations.

Test at least:

1. Complete case.
2. Case with missing fields.
3. Consumer case.
4. Merchant case.
5. Agent/tool failure.

## Knowledge Integration

When infrastructure is available:

- connect to PostgreSQL
- verify database access
- insert/retrieve case data
- perform vector retrieval
- connect to Neo4j
- execute a basic knowledge query

Tests should be marked appropriately, for example:

```python
@pytest.mark.integration
```

Integration tests should be skippable when Docker infrastructure is unavailable.

---

# 36. Phase 33 — README

Create a useful `README.md`.

Include:

## Overview

Explain the platform architecture.

## Architecture

Show:

```text
Phone / Email / Document / API
            ↓
        FastAPI Gateway
            ↓
      Event Normalization
            ↓
        LangGraph
            ↓
 ┌──────────┼───────────┐
 ↓          ↓           ↓
Agents     MCP       Knowledge
 ↓          ↓           ↓
Classification
Enrichment
Gap Analysis
Communication
            ↓
      Case Update Service
            ↓
PostgreSQL / Neo4j / pgvector
```

## Local Setup

Document:

```bash
git clone ...
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

For Windows also provide the appropriate activation command.

## Environment

Explain:

```bash
cp .env.example .env
```

and configuration categories.

## Infrastructure

```bash
docker compose up -d
```

## Run Application

```bash
uvicorn src.main:app --reload
```

## Testing

```bash
pytest
```

and:

```bash
pytest -m integration
```

## Code Quality

Document Ruff/type-check commands.

## API

Document the initial health and ingestion endpoints.

## Architecture Decisions

Explain why:

- LangGraph handles orchestration.
- Agents contain specialized AI behavior.
- MCP adapters isolate enterprise systems.
- Neo4j handles graph knowledge/rules.
- PostgreSQL handles durable relational state.
- pgvector handles semantic retrieval.
- Redis handles transient/cache use cases.

---

# 37. Phase 34 — Git Configuration

Create `.gitignore`.

Ignore at minimum:

```text
.venv/
__pycache__/
*.pyc
.env
.pytest_cache/
.mypy_cache/
.ruff_cache/
.coverage
htmlcov/
dist/
build/
*.egg-info/
.idea/
.vscode/
.DS_Store
```

Do not ignore source files, tests, Docker configuration, or `.env.example`.

---

# 38. Phase 35 — Dependency Injection

Introduce lightweight dependency factories for:

- settings
- database clients
- Neo4j client
- Redis client
- MCP client
- AI model client
- agents
- services
- LangGraph application

The goal is to make production implementations replaceable with mocks/fakes during tests.

---

# 39. Phase 36 — Error Handling

Create structured exceptions where appropriate.

At minimum distinguish:

```text
ConfigurationError
MCPConnectionError
MCPRequestError
KnowledgeRetrievalError
AgentExecutionError
CaseProcessingError
ValidationError
```

Map API-facing exceptions to appropriate HTTP responses.

Do not expose internal stack traces or secrets through API responses.

---

# 40. Phase 37 — Observability Foundations

Add basic observability fields:

```text
request_id
correlation_id
case_id
thread_id
agent_name
operation
duration
status
```

Every major workflow execution should be traceable through the correlation ID.

Do not implement a full distributed tracing platform unless explicitly requested.

---

# 41. Phase 38 — Idempotency

Design ingestion and case update operations to support idempotency.

The same event should not accidentally create duplicate cases or duplicate updates.

Use:

```text
event_id
idempotency_key
case_id
correlation_id
```

where applicable.

Persist enough information to safely detect duplicate processing.

---

# 42. Phase 39 — Application Startup Validation

At startup:

1. Load configuration.
2. Initialize logging.
3. Validate configuration.
4. Initialize clients.
5. Compile LangGraph.
6. Register routes.
7. Expose readiness status.

Avoid failing startup solely because an optional external MCP endpoint is unavailable in local development.

Required infrastructure dependencies should be configurable.

---

# 43. Phase 40 — Initial End-to-End Flow

Create a minimal executable flow:

```text
POST /events
       ↓
Normalize event
       ↓
Create initial CaseState
       ↓
Invoke LangGraph
       ↓
Classification agent
       ↓
Enrichment agent
       ↓
Gap analysis agent
       ↓
Decision router
       ↓
Update case service OR communication agent
       ↓
Return processing status
```

For external dependencies that do not yet exist, use mock adapters behind interfaces.

The end-to-end flow must be executable locally.

---

# 44. Phase 41 — Do Not Over-Implement

Do not implement the following unless explicitly required:

- Real enterprise credentials.
- Real production MCP APIs.
- Real email delivery.
- Complex domain-specific CRD rules.
- Production-grade authentication/authorization.
- Full frontend/UI.
- Kubernetes deployment.
- Complex event streaming infrastructure.
- Detailed business-specific prompts.
- Large synthetic datasets.
- Production migration infrastructure beyond what is needed for the initial schema.

The objective is a strong, extensible foundation.

---

# 45. Phase 42 — Code Quality Requirements

Before completing the task, verify:

```bash
python -m compileall src config
pytest
ruff check .
ruff format --check .
```

If MyPy is configured:

```bash
mypy src
```

Fix all avoidable errors.

Avoid placeholder implementations that silently return incorrect production-looking data.

Use explicit mock/stub behavior where an external integration is not available.

---

# 46. Phase 43 — Final Validation Checklist

The implementation is complete only when all of the following are true:

- [ ] Repository structure exists.
- [ ] Python package configuration works.
- [ ] `.env.example` exists.
- [ ] `.gitignore` exists.
- [ ] FastAPI starts.
- [ ] `/health` works.
- [ ] `/ready` works.
- [ ] Gateway schemas exist.
- [ ] Phone/email/document normalizers exist.
- [ ] LangGraph state is defined.
- [ ] LangGraph graph compiles.
- [ ] Conditional routing exists.
- [ ] Checkpoint abstraction exists.
- [ ] Base agent abstraction exists.
- [ ] Classification agent exists.
- [ ] Enrichment agent exists.
- [ ] Gap analysis agent exists.
- [ ] Communication agent exists.
- [ ] Case update service exists.
- [ ] MCP client abstraction exists.
- [ ] CLIC MCP adapter exists.
- [ ] Griffin MCP adapter exists.
- [ ] Merchant MCP adapter exists.
- [ ] Consumer MCP adapter exists.
- [ ] Document processing MCP adapter exists.
- [ ] Neo4j client exists.
- [ ] Neo4j query abstraction exists.
- [ ] PostgreSQL client exists.
- [ ] PostgreSQL models exist.
- [ ] pgvector client exists.
- [ ] Embedding abstraction exists.
- [ ] Redis configuration exists.
- [ ] Security utilities exist.
- [ ] Dockerfile exists.
- [ ] Docker Compose exists.
- [ ] Unit tests exist.
- [ ] Integration tests exist.
- [ ] README contains setup instructions.
- [ ] No real credentials are committed.
- [ ] No hard-coded environment-specific endpoints exist.
- [ ] External integrations are mockable.
- [ ] Basic end-to-end mocked flow works.
- [ ] Code quality checks pass.

---

# 47. Expected Deliverable

At the end of this task, the repository must be a **working architectural foundation**, not merely an empty folder structure.

A developer should be able to:

```bash
docker compose up -d
```

then:

```bash
cp .env.example .env
```

then:

```bash
pip install -e .
```

and finally:

```bash
uvicorn src.main:app --reload
```

and access:

```text
GET /health
GET /ready
POST /events
POST /events/phone
POST /events/email
POST /events/document
```

The LangGraph workflow must compile and execute using mocked/stubbed external dependencies.

The project must be structured so that real MCP endpoints, AI models, Neo4j knowledge, PostgreSQL persistence, and pgvector retrieval can be connected later without redesigning the architecture.

---

# 48. Recommended Implementation Order

Implement in this order:

```text
1. Repository scaffolding
2. pyproject.toml
3. Configuration/settings
4. Logging
5. FastAPI application
6. Gateway schemas + normalizers
7. PostgreSQL abstraction
8. Neo4j abstraction
9. Redis abstraction
10. MCP client abstraction
11. MCP adapters
12. AI/model abstraction
13. Agent base
14. Classification agent
15. Enrichment agent
16. Gap analysis agent
17. Communication agent
18. Case update service
19. LangGraph state
20. Router
21. Checkpointing
22. Graph assembly
23. End-to-end gateway → graph flow
24. Unit tests
25. Integration tests
26. Docker configuration
27. README
28. Static checks
29. Final validation
```

---

# 49. Important Architectural Constraint

Maintain this dependency direction:

```text
gateway
   ↓
orchestration
   ↓
agents
   ↓
services / abstractions
   ↓
mcp_tools / knowledge
```

Avoid dependencies flowing upward.

For example:

- MCP adapters must not import LangGraph.
- Database clients must not import agents.
- Agents should not directly instantiate database connections.
- Route handlers should not contain business logic.
- LangGraph nodes should call agents/services rather than contain all implementation details.
- Configuration should be centralized.

This constraint is critical for future expansion.

---

# 50. Definition of Done

The task is considered complete when:

1. The requested architecture is physically created.
2. The application starts successfully.
3. The API responds successfully.
4. The LangGraph workflow compiles.
5. A mocked end-to-end case can pass through the workflow.
6. Database/MCP/AI dependencies are abstracted and replaceable.
7. Docker Compose starts local infrastructure.
8. Unit tests pass without external enterprise systems.
9. Integration tests are available and appropriately isolated.
10. Configuration and secrets are environment-driven.
11. README explains how to run and extend the project.
12. No major architectural component is represented only by an empty placeholder.
13. The codebase is ready for the next development phase: implementing real business rules, MCP contracts, AI prompts/models, CRD schemas, persistence details, and production integrations.
