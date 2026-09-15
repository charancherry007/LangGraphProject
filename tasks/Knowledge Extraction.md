# Task 2 — Knowledge Extraction, CRD Enrichment & Intelligent Gap Discovery

## Mission

Enhance the **existing AI Case Processing Platform** to perform accurate:

1. Case classification
2. Knowledge-aware CRD extraction
3. Multi-source attribute enrichment
4. Master-requirement vs extracted-data comparison
5. Missing field/document discovery
6. Conflict detection
7. Phone/call real-time follow-up generation
8. Email consolidated follow-up generation

This task consumes the knowledge/database layer from Task 1.

**Do not rewrite the existing platform.** GPT-6 Astra is the coding/engineering agent: it must analyze first, identify reusable code blocks/functions, and then implement the smallest safe extensions.

---

## 1. Analyze Before Coding

Inspect the complete repository and the Task 1 implementation before changing code.

Review:

- case classifier
- enrichment agent
- gap analysis agent
- communication agent
- LangGraph state/graph/router
- knowledge retrieval service
- Neo4j/PostgreSQL/PGvector wrappers
- MCP adapters/client
- model/LLM abstraction
- prompts
- structured output schemas
- tests

Search for existing functions/classes that already implement part of the requested behavior.

Do not create duplicate:

```text
classifier
enrichment pipeline
gap engine
graph
database client
MCP client
model client
```

unless the analysis proves it is necessary.

Follow:

```text
ANALYZE → MAP → REUSE → EXTEND → TEST → REGRESSION CHECK
```

---

## 2. Target Knowledge-Aware Pipeline

Extend the existing pipeline to:

```text
Incoming Inquiry
      ↓
Normalize
      ↓
Retrieve Knowledge Candidates
      ↓
Case Classifier
      ↓
Retrieve Authoritative CRD Requirements
      ↓
Retrieve Context
      ↓
Enrichment / Attribute Extraction
      ↓
Deterministic Requirement Diff
      ↓
Gap Analysis / Decision
      ↓
Channel-Specific Follow-Up
      ├── Phone
      ├── Email
      └── Complete → Existing Case Update
```

Preserve existing nodes and routes wherever possible.

---

## 3. Case Classifier Agent

Use the actual taxonomy stored in Neo4j and semantic knowledge in PGvector to identify:

```text
Case Type
Market
Line of Business
Channel
Confidence
```

Examples such as product upgrade/downgrade, maintenance, or bank account changes are illustrative only. Use actual KB values.

---

## 4. Candidate Retrieval

Do not ask the model to classify against an unlimited universe.

Use:

```text
Neo4j structured retrieval
+
PGvector semantic retrieval
↓
Merged candidates
↓
LLM classification
```

Reuse Task 1's `KnowledgeRetrievalService`.

---

## 5. Classification Guardrails

The classifier must:

- select known taxonomy values
- not invent case types, markets, LOBs, or channels
- preserve explicit incoming metadata
- distinguish explicit vs inferred metadata
- return confidence
- support UNKNOWN/UNCLASSIFIED when evidence is insufficient and the existing architecture supports it

Do not silently convert low confidence into a valid classification.

---

## 6. CRD Requirement Retrieval

After classification, retrieve authoritative requirements from Neo4j:

```text
Case Type
   ↓
CRD
   ↓
Required Fields
   ↓
Allowed Values
   ↓
Required Documents
   ↓
Conditional Requirements
   ↓
Validation Rules
```

The graph is authoritative for requirements.

The LLM must not invent required fields/documents.

---

## 7. Enrichment Agent

Extract relevant case attributes from available sources:

```text
customer input
email
phone transcript
historical case notes
documents
MCP responses
existing case data
```

Reuse existing context models/state. Do not duplicate information already represented in LangGraph state.

---

## 8. Multi-Source Context

Normalize available evidence into a common structure where needed:

```text
CaseContext
 ├── customer_input
 ├── emails
 ├── transcript
 ├── historical_notes
 ├── documents
 ├── MCP_context
 └── existing_case_data
```

Reuse existing models instead of introducing duplicate context structures.

---

## 9. Relevant Attribute Extraction

Only extract fields relevant to the classified case's requirements.

For each requirement determine:

```text
PRESENT
MISSING
UNKNOWN
CONFLICTING
NOT_APPLICABLE
INVALID
```

Example values are illustrative only.

Do not treat vague inference as verified data unless existing validation rules permit it.

---

## 10. Structured Extraction Output

Prefer Pydantic/structured model output.

Conceptually:

```json
{
  "attributes": [
    {
      "field": "account_type",
      "value": "checking",
      "status": "present",
      "confidence": 0.98,
      "evidence": []
    }
  ]
}
```

Reuse the existing output schema if compatible. Avoid regex parsing of free-form LLM responses.

---

## 11. Evidence / Provenance

Where practical, every important extracted value should retain:

```text
field
value
source_type
source_id
confidence
evidence reference
```

Possible sources:

```text
email
transcript
document
MCP response
case note
customer input
```

Do not log sensitive evidence.

---

## 12. Historical Context

Use PGvector to retrieve semantically similar:

```text
historical cases
transcripts
case notes
emails
```

Historical information is supporting context only.

The current knowledge graph remains authoritative for:

```text
taxonomy
required fields
required documents
validation rules
```

Historical cases must never silently redefine current requirements.

---

## 13. MCP Context

Use existing MCP architecture:

```text
Enrichment Agent
      ↓
MCP Adapter
      ↓
Shared MCP Client
      ↓
MCP Server
```

Reuse CLIC, Griffin, Merchant, Consumer, and Document Processing adapters as appropriate.

Do not directly call external APIs from the agent.

---

## 14. Document Extraction

When document-processing context is available:

1. retrieve OCR/IDP output
2. extract relevant entities
3. map them to CRD fields
4. preserve provenance
5. validate document type against knowledge requirements

A file's existence alone must not satisfy a document requirement.

---

## 15. Deterministic Requirement Satisfaction Engine

The master-vs-case comparison must primarily be deterministic.

Input:

```text
Master Requirements
+
Extracted Attributes
+
Document Evidence
```

Output:

```text
Satisfied
Missing
Conflicting
Invalid
Not Applicable
```

Use the LLM for semantic reasoning and wording, not for basic requirement presence checks.

---

## 16. Graph Diff / Gap Discovery

Perform:

```text
Knowledge Graph Master Requirements
                 VS
         Enriched Case Data
                 ↓
                DIFF
```

Conceptually:

```python
for requirement in master_requirements:
    extracted = enriched_attributes.get(requirement.field)

    if satisfies(requirement, extracted):
        mark_present()
    elif conflicts(requirement, extracted):
        mark_conflicting()
    else:
        mark_missing()
```

Adapt this to the actual project schema and existing validation engine.

---

## 17. Requirement Types

Support the requirement types actually present in the KB, potentially including:

```text
required field
optional field
required document
conditional field
conditional document
allowed value
format validation
cross-field validation
```

Do not hard-code domain-specific conditions.

---

## 18. Conditional Requirements

For each conditional requirement:

1. evaluate its condition using current extracted data
2. determine whether it applies
3. only then mark it missing/present

Do not report an inapplicable conditional requirement as missing.

---

## 19. Missing Fields

Return missing fields separately:

```text
missing_fields
```

Where supported, include:

```text
field
display_name
reason
requirement_id
priority
```

Use only metadata supported by the knowledge model.

---

## 20. Missing Documents

Return missing documents separately:

```text
missing_documents
```

Where supported, include:

```text
document_type
reason
requirement_id
priority
```

Never invent document names.

---

## 21. Conflicting Attributes

Detect contradictory information across sources.

Example:

```text
Email: account_type = checking
MCP:   account_type = savings
```

Return a structured conflict with provenance.

Do not silently select a value unless existing precedence/business rules explicitly permit it.

---

## 22. Invalid Attributes

Where validation rules exist, detect:

```text
invalid format
invalid allowed value
invalid relationship
cross-field inconsistency
```

An invalid value should not be incorrectly reported as merely missing.

---

## 23. Gap Analysis / Decision Agent

The agent receives:

```text
master requirements
extracted attributes
document evidence
validation results
conflicts
```

Its role is to reason about ambiguity, prioritization, and clarification wording.

It must not invent requirements.

The deterministic requirement evaluator remains authoritative for whether something is missing.

---

## 24. Gap Analysis Result

Reuse/extend the existing state model with a structure similar to:

```text
GapAnalysisResult
 ├── complete
 ├── missing_fields
 ├── missing_documents
 ├── conflicting_attributes
 ├── invalid_attributes
 ├── satisfied_requirements
 ├── follow_up_items
 └── decision
```

Do not remove existing state fields.

---

## 25. Phone / Real-Time Follow-Up

For:

```text
channel = PHONE
```

generate immediate next questions/actions.

Conceptual structure:

```text
NextAction
-----------
type: ASK
question: "Could you confirm ...?"
reason: "Required for ..."
requirement_id: "..."
priority: "..."
```

Questions must be:

- concise
- conversational
- grounded in actual missing requirements
- one logical question at a time
- ordered by dependency/priority

---

## 26. Real-Time Incremental Context

For phone conversations, when a new transcript segment arrives:

```text
new transcript segment
       ↓
incremental extraction
       ↓
update attributes
       ↓
re-run requirement diff
       ↓
generate next question
```

Reuse existing LangGraph checkpoint/thread state where available.

Avoid unnecessarily restarting the entire case.

---

## 27. Avoid Repeated Questions

Before generating a phone question, check:

```text
current extracted state
follow-up history
already verified documents
previous questions
```

Never ask again for information that has already been satisfied or answered.

---

## 28. Email Follow-Up

For:

```text
channel = EMAIL
```

generate one consolidated response using:

```text
missing fields
missing documents
conflicts
clarifications
```

The response should:

- group related requests
- avoid duplicates
- clearly explain what is required
- list required documents
- avoid requesting already satisfied data
- remain professional and customer-friendly

---

## 29. Email Guardrails

Email generation may use only:

```text
actual knowledge requirements
+
actual gap analysis
```

It must not invent:

```text
documents
fields
deadlines
fees
policies
```

unless explicitly provided by the knowledge/context layer.

---

## 30. Follow-Up Deduplication

Before LLM wording:

```text
normalize gaps
 ↓
deduplicate
 ↓
group related requirements
 ↓
generate wording
```

If one document/evidence item can satisfy multiple requirements, consolidate the request appropriately.

---

## 31. LLM vs Deterministic Responsibilities

Use the LLM for:

```text
semantic classification
ambiguous language interpretation
attribute extraction
ambiguous conflict reasoning
natural-language phone questions
natural-language email generation
```

Use deterministic code/knowledge for:

```text
taxonomy validation
requirement lookup
requirement diff
missing detection
document detection
allowed-value validation
deduplication
routing
persistence
```

This separation is mandatory.

---

## 32. Channel Router

Reuse the existing router.

Conceptually:

```text
Gap Analysis
     ↓
Is Complete?
 ┌───┴────┐
Yes       No
 │         │
 ▼         ▼
Update   Channel Router
Case      ├── PHONE
          └── EMAIL
```

Do not create a second routing implementation.

---

## 33. LangGraph State Extension

Extend the existing state without removing fields.

Potential fields:

```text
knowledge_candidates
classification_result
crd_requirements
extracted_attributes
attribute_evidence
document_evidence
validation_results
missing_fields
missing_documents
conflicting_attributes
invalid_attributes
gap_analysis
follow_up_questions
follow_up_email
follow_up_history
```

Use backward-compatible defaults.

---

## 34. Failure Semantics

If MCP context is unavailable, distinguish:

```text
NOT FOUND
vs
NOT AVAILABLE
```

Do not mark unavailable data as customer-missing data.

If authoritative knowledge requirements cannot be retrieved:

```text
DO NOT assume requirements
DO NOT generate unsupported follow-up
DO NOT mark the case complete
```

Use the existing safe error/manual-review route.

---

## 35. Testing

Run all existing tests before changes and establish a baseline.

Add tests for:

### Classification

```text
known case type
unknown case type
ambiguous case
low confidence
metadata classification
graph candidates
vector candidates
```

### Enrichment

```text
attribute present
attribute missing
attribute conflicting
attribute invalid
document evidence
historical context
MCP context
```

### Gap Analysis

```text
complete case
missing field
missing document
conditional requirement
invalid value
conflicting value
```

### Phone

```text
single missing field
multiple missing fields
duplicate prevention
incremental transcript
```

### Email

```text
single gap
multiple gaps
field + document gaps
deduplication
no unnecessary requests
```

---

## 36. Golden Test Fixtures

Create synthetic fixtures based on the actual knowledge base:

```text
complete_case.json
missing_required_field.json
missing_required_document.json
conditional_requirement.json
conflicting_information.json
invalid_attribute.json
phone_followup.json
email_followup.json
```

Do not use real customer PII.

---

## 37. Regression Testing

After implementation:

```bash
pytest
```

must pass for all existing tests.

Also verify:

```text
existing API endpoints
existing LangGraph execution
existing MCP adapters
existing database operations
existing model providers
```

continue to work.

---

## 38. Observability

Reuse existing logging/telemetry and add structured events for:

```text
classification
knowledge retrieval
enrichment
requirement evaluation
gap discovery
follow-up generation
```

Include:

```text
correlation_id
case_id
operation
duration
status
```

Never log secrets or unnecessary customer-sensitive payloads.

---

## 39. Performance

Avoid:

```text
entire-graph retrieval
every historical case retrieval
unnecessary LLM calls
N+1 database queries
full re-enrichment when incremental state is possible
```

Prefer targeted graph queries, top-k vector retrieval, incremental updates, and caching of stable requirements where existing infrastructure supports it.

---

## 40. Acceptance Criteria

- [ ] Repository analyzed before implementation.
- [ ] Existing functions/classes reused wherever practical.
- [ ] Existing classifier extended/reused.
- [ ] Neo4j taxonomy used for classification candidates.
- [ ] PGvector used for semantic candidates.
- [ ] Case Type returned.
- [ ] Market returned.
- [ ] LOB returned.
- [ ] Channel returned.
- [ ] Confidence returned.
- [ ] CRD requirements come from authoritative knowledge.
- [ ] Required fields/documents/rules retrieved.
- [ ] Customer input enriched.
- [ ] Historical notes/transcripts/emails/documents/MCP context supported where applicable.
- [ ] Attribute provenance preserved.
- [ ] Requirement diff is deterministic.
- [ ] Missing fields identified.
- [ ] Missing documents identified.
- [ ] Conflicts identified.
- [ ] Invalid attributes identified where rules exist.
- [ ] Conditional requirements handled.
- [ ] Phone follow-up questions generated.
- [ ] Repeated phone questions prevented.
- [ ] Email follow-up consolidated.
- [ ] Email does not invent requirements.
- [ ] Existing case-update path remains functional.
- [ ] Existing graph is extended, not duplicated.
- [ ] Existing regression tests pass.
- [ ] New tests pass.

---

## 41. Final Engineering Review

Before completion, inspect the final diff for:

### Reuse

- existing functions/classes reused
- existing model abstraction reused
- existing MCP architecture reused
- existing database wrappers reused
- existing LangGraph nodes reused

### Correctness

- graph is authoritative for requirements
- LLM does not invent requirements
- missing vs unavailable is distinguished
- historical context does not redefine current requirements
- conflicts are surfaced
- follow-ups are grounded in actual gaps

### Regression

- existing endpoints unchanged
- existing state fields preserved
- existing agents remain functional
- existing MCP adapters remain functional
- existing DB behavior remains functional
- existing tests pass

---

## 42. Final End-to-End Scenario

Run a synthetic case through:

```text
Customer Inquiry
      ↓
Gateway
      ↓
Existing Normalization
      ↓
Neo4j + PGvector Candidate Retrieval
      ↓
Case Classifier
      ↓
Case Type + Market + LOB + Channel
      ↓
Neo4j CRD Requirement Retrieval
      ↓
Historical / Email / Transcript / Document / MCP Context
      ↓
Enrichment Agent
      ↓
Extracted Attributes + Evidence
      ↓
Deterministic Requirement Diff
      ↓
Gap Analysis
      ↓
       ┌─────────────────────┐
       │                     │
   Complete                Gaps
       │                     │
       ▼                     ▼
Existing Update       Channel Router
                            │
                     ┌──────┴──────┐
                     ▼             ▼
                   Phone         Email
                     │             │
                     ▼             ▼
                Next Question   Consolidated
                / Action        Follow-up
```

The flow must be executable with synthetic test data and the existing application's architecture.

---

## 43. Definition of Done

The enhancement is complete when the knowledge-aware pipeline works end-to-end and existing functionality remains intact:

```text
Knowledge
   ↓
Classification
   ↓
CRD Requirements
   ↓
Extraction
   ↓
Requirement Diff
   ↓
Gap Discovery
   ↓
Channel-Specific Follow-Up
```

The system must be **knowledge-grounded, deterministic where possible, LLM-assisted where useful, MCP-compatible, testable, and backward-compatible**.
