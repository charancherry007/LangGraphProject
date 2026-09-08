# Task — Enhance Existing LangGraph Project for Real-Time Voice Processing, Process Detection & Mandatory Field Retrieval

## Objective

Analyze the existing LangGraph repository and enhance the existing codebase to support real-time voice/customer-care conversation processing without unnecessarily rewriting or duplicating existing functionality.

The existing project already extracts information from transcriptions, images, and documents and maps extracted information to process-related mandatory fields. Reuse that implementation wherever possible.

The new capability must:

1. Consume conversation transcript events in near real time.
2. Understand the customer's issue/request as the conversation progresses.
3. Identify the relevant business process/process name.
4. Retrieve the process context/definition.
5. Retrieve mandatory and optional fields for that process.
6. Incrementally extract fields from the conversation.
7. Compare captured fields with required process fields.
8. Continuously update the missing-field list.
9. Display the process, captured fields, missing mandatory fields, and optional fields in the existing Streamlit chat UI.
10. Suggest the next information the customer-care agent needs to obtain.

The implementation must be an enhancement of the existing LangGraph repository, not a separate application.

---

## 1. Analyze Existing Repository First

Before changing code, perform a complete repository analysis.

Identify and document:

- Application entry points.
- Existing LangGraph graph and nodes.
- Existing state models.
- Existing transcription ingestion.
- Existing image/document ingestion.
- Existing OCR/IDP functionality.
- Existing extraction agents/services.
- Existing LLM gateway and model configuration.
- Existing prompts.
- Existing process identification logic.
- Existing process-to-field mapping.
- Existing mandatory/optional field definitions.
- Existing knowledge/context retrieval.
- Existing RAG/vector-store implementation, if any.
- Existing Streamlit UI/chat implementation.
- Existing API/integration layer.
- Existing persistence.
- Existing tests.
- Existing configuration/secrets handling.

The known existing architecture should be reused where applicable. The repository previously used modular areas such as `src/config`, `src/models`, `src/ingestion`, `src/extraction`, `src/knowledge`, `src/graph`, `src/utils`, and `src/ui`; verify the actual current repository before making assumptions.

Do not create replacement implementations when an equivalent component already exists.

### Required analysis document

Create:

```text
docs/realtime_voice_architecture.md
```

Include:

- Existing architecture.
- Relevant files/classes/functions.
- Current data flow.
- Current LangGraph state.
- Current extraction flow.
- Current process/field mapping flow.
- Current knowledge retrieval flow.
- Current Streamlit flow.
- Gaps required for realtime processing.
- Exact files to modify.
- New files required and why.
- Reuse strategy for each existing component.

Create a table similar to:

| Component | Existing Path | Current Purpose | Reuse/Extend Strategy |
|---|---|---|---|
| Extraction | ... | ... | Reuse |
| Process Mapping | ... | ... | Extend |
| Knowledge Retrieval | ... | ... | Reuse |
| LangGraph State | ... | ... | Extend |
| Streamlit UI | ... | ... | Extend |

---

## 2. Target User Experience

The target experience is a customer-care call.

Example:

```text
Customer:
"I want to cancel my credit card because I don't use it anymore."

        ↓

Realtime transcript
        ↓

AI identifies:
Intent: Card Cancellation
Process: Credit Card Cancellation

        ↓

Chat UI:

Detected Process
Credit Card Cancellation
Confidence: 96%

Mandatory Fields
✓ Customer Name
✓ Account Number
✗ Effective Date

Optional Fields
○ Cancellation Reason
○ Additional Comments
```

As the conversation continues:

```text
Customer:
"My name is John Smith and my account number is 123456789. I'd like it cancelled immediately."

        ↓

Updated UI:

Mandatory Fields
✓ Customer Name
✓ Account Number
✓ Effective Date / Immediate cancellation captured

Optional Fields
○ Cancellation Reason
○ Additional Comments

Status:
Ready for validation
```

The UI must update incrementally as new final transcript segments arrive.

---

## 3. Real-Time Transcript Event Model

Use an event-based model.

Example:

```json
{
  "session_id": "CALL-10001",
  "sequence": 12,
  "speaker": "customer",
  "text": "I want to cancel my credit card",
  "timestamp": "2026-09-08T10:20:00Z",
  "is_final": true
}
```

Support:

- Customer utterances.
- Agent utterances.
- Partial transcript events.
- Final transcript events.
- Session/conversation ID.
- Sequence number.
- Timestamp.

Do not treat every partial transcript event as a new complete request.

If the repository already has a transcription streaming interface, reuse it.

If realtime speech-to-text integration does not exist, create a provider-neutral adapter/interface rather than coupling LangGraph nodes to a specific telephony/STT vendor.

Conceptual interface:

```python
class RealtimeTranscriptProvider:
    async def receive_events(self):
        ...
```

The provider itself should remain configurable.

---

## 4. Extend Existing LangGraph State

Extend the existing LangGraph state rather than introducing a parallel workflow state.

The state must be capable of maintaining:

```text
conversation_id
transcript_events
conversation_transcript
current_intent
candidate_processes
identified_process
process_confidence
process_context
mandatory_fields
optional_fields
captured_fields
missing_mandatory_fields
missing_optional_fields
ambiguous_fields
conflicting_fields
field_confidence
next_required_fields
processing_status
```

Use the repository's existing Pydantic/state models where possible.

Do not duplicate schemas already present in the repository.

---

## 5. Realtime Processing Flow

Implement an event-driven processing flow similar to:

```text
Voice Call / Existing STT
        ↓
Transcript Event
        ↓
Update Conversation State
        ↓
Intent Detection
        ↓
Process Identification
        ↓
Process Context Retrieval
        ↓
Incremental Field Extraction
        ↓
Mandatory/Optional Field Evaluation
        ↓
Build Agent Context
        ↓
Update Streamlit Chat UI
        ↓
Wait for Next Transcript Event
```

Do not continuously poll in a tight CPU loop.

Use the existing LangGraph streaming/event capabilities if available.

---

## 6. Intent and Process Identification

The implementation must be compatible with dynamically identifying the process name from the conversation.

Do not hard-code the application to cancellation only.

The flow must support:

```text
Conversation
   ↓
Intent
   ↓
Process Identification
   ↓
Process Name
   ↓
Process Context
   ↓
Mandatory + Optional Fields
```

Example result:

```json
{
  "intent": "Cancel Credit Card",
  "process": {
    "name": "Credit Card Cancellation",
    "confidence": 0.96
  }
}
```

If multiple processes are plausible, preserve candidates instead of forcing a selection:

```json
{
  "candidate_processes": [
    {
      "name": "Credit Card Cancellation",
      "confidence": 0.82
    },
    {
      "name": "Account Closure",
      "confidence": 0.61
    }
  ],
  "status": "AMBIGUOUS"
}
```

Reuse existing process-identification functionality if available.

---

## 7. Process Context Retrieval

Reuse the existing knowledge/context retrieval mechanism.

The retrieval layer must be able to provide, for a selected process:

- Process name.
- Process description.
- Process purpose.
- Mandatory fields.
- Optional fields.
- Field descriptions.
- Field types.
- Validation requirements.
- Related terminology/synonyms.
- Process-specific instructions where available.

Conceptual interface:

```python
retrieve_process_context(process_name)
```

Example:

```json
{
  "process_name": "Credit Card Cancellation",
  "description": "...",
  "mandatory_fields": [
    {
      "name": "Customer Name",
      "type": "Text",
      "description": "..."
    },
    {
      "name": "Account Number",
      "type": "Identifier",
      "description": "..."
    },
    {
      "name": "Effective Date",
      "type": "Date",
      "description": "..."
    }
  ],
  "optional_fields": [
    {
      "name": "Cancellation Reason",
      "type": "Text"
    }
  ]
}
```

The actual schema must come from the existing process metadata/mapping implementation.

---

## 8. Incremental Field Extraction

When a new customer transcript segment arrives, extract information incrementally.

The extractor should use:

```text
Existing Conversation State
+
New Transcript Segment
+
Current Process Context
        ↓
Incremental Extraction
```

Do not reprocess the complete conversation unnecessarily on every event.

Example:

```text
Utterance 1:
"I want to cancel my card."

→ Process identified

Utterance 2:
"My name is John Smith."

→ Customer Name captured

Utterance 3:
"Account number is 123456789."

→ Account Number captured
```

The new extraction must merge with existing values using the repository's existing merge/conflict logic where available.

---

## 9. Mandatory and Optional Field Tracking

Every process field should have a clear state.

Recommended statuses:

```text
CAPTURED
MISSING
OPTIONAL_MISSING
LOW_CONFIDENCE
AMBIGUOUS
CONFLICT
```

Example:

```json
{
  "name": "Account Number",
  "type": "Identifier",
  "required": true,
  "value": "123456789",
  "status": "CAPTURED",
  "confidence": 0.98
}
```

Missing:

```json
{
  "name": "Effective Date",
  "required": true,
  "value": null,
  "status": "MISSING",
  "confidence": 0.0
}
```

Mandatory and optional fields must never be mixed in the UI or decision logic.

---

## 10. Conflict Handling

If the customer provides different values for the same field, do not silently overwrite the previous value.

Example:

```text
Customer:
"My account number is 123456789."

Later:
"Actually, it is 123456780."
```

Result:

```json
{
  "field": "Account Number",
  "status": "CONFLICT",
  "values": [
    "123456789",
    "123456780"
  ]
}
```

Reuse the repository's existing conflict-resolution/provenance implementation where available.

---

## 11. Next Required Information

The system should calculate the next information the customer-care agent needs to obtain.

Example:

```text
Missing mandatory information:

1. Effective Date
2. Cancellation Reason
```

If only one mandatory field is missing:

```text
Next required field:
Effective Date
```

Optionally generate an agent-facing clarification question from the process field definition.

Example:

```text
Could you please confirm the date you would like the cancellation to take effect?
```

The question must be generated from retrieved process metadata and must not invent requirements.

---

## 12. Realtime Optimization

Minimize latency and unnecessary model calls.

Implement where appropriate:

- Partial/final transcript distinction.
- Debouncing of partial events.
- Incremental extraction.
- Process-context caching.
- Avoiding repeated process retrieval after the process is stable.
- Avoiding full-conversation reprocessing.
- Reusing previously extracted fields.
- Event sequence/idempotency checks.

Recommended strategy:

```text
Partial transcript
       ↓
Lightweight UI update

Final transcript
       ↓
LangGraph processing
```

Use the existing STT event semantics if available.

---

## 13. Context Caching

Once a process is confidently identified, cache its process context for the conversation.

Example:

```text
Process = Credit Card Cancellation
        ↓
Retrieve Context Once
        ↓
Cache in Conversation State
```

Do not retrieve identical context after every utterance.

Refresh only when:

- Process changes.
- Process becomes ambiguous.
- Context version changes.
- Explicit refresh is requested.

Reuse existing cache mechanisms if available.

---

## 14. Streamlit Chat UI

Reuse the existing Streamlit UI where available.

Enhance it to show:

### Conversation

```text
Customer:
I want to cancel my credit card.

Agent:
I can help with that.
```

### Detected Process

```text
Detected Process
Credit Card Cancellation
Confidence: 96%
```

### Mandatory Fields

```text
Mandatory Fields

✓ Customer Name
✓ Account Number
✗ Effective Date
```

### Optional Fields

```text
Optional Fields

○ Cancellation Reason
○ Additional Comments
```

### Field Details

Where useful, display:

- Field name.
- Current value.
- Status.
- Confidence.
- Source transcript segment.

The UI must update when new transcript events are processed.

---

## 15. Structured UI Context

Expose a structured object to the UI.

Example:

```json
{
  "process_name": "Credit Card Cancellation",
  "process_confidence": 0.96,
  "mandatory_fields": [
    {
      "name": "Customer Name",
      "status": "CAPTURED",
      "value": "John Smith"
    },
    {
      "name": "Account Number",
      "status": "CAPTURED",
      "value": "123456789"
    },
    {
      "name": "Effective Date",
      "status": "MISSING",
      "value": null
    }
  ],
  "optional_fields": [
    {
      "name": "Cancellation Reason",
      "status": "OPTIONAL_MISSING",
      "value": null
    }
  ],
  "next_required_fields": [
    "Effective Date"
  ],
  "ready_for_validation": false
}
```

Use existing project schemas if equivalent models already exist.

---

## 16. Confidence Handling

Maintain separate confidence values for:

- Intent.
- Process.
- Individual fields.

Example:

```text
Intent:       0.95
Process:      0.91
Account No:   0.99
Date:         0.72
```

A low-confidence value must not be treated as confirmed.

Reuse the existing confidence thresholds/configuration.

---

## 17. API / Integration Boundary

If the repository already contains an API/event layer, extend it rather than creating a parallel API.

If a new boundary is required, use a provider-neutral design.

Conceptual interfaces may include:

```text
POST /realtime/session
POST /realtime/transcript
GET  /realtime/session/{session_id}/context
```

These are conceptual only; follow the repository's existing architecture and conventions.

Do not place telephony/STT-specific logic inside LangGraph business nodes.

---

## 18. Backward Compatibility

Existing functionality must continue to work.

Do not break:

- transcription extraction
- image extraction
- document extraction
- existing process mapping
- existing mandatory-field mapping
- existing knowledge persistence
- existing LangGraph workflows
- existing Streamlit workflows
- existing model providers

Run the existing test suite before and after implementation.

---

## 19. Testing

Add tests for:

### Repository Reuse

- Existing extraction continues to work.
- Existing process mapping continues to work.
- Existing knowledge retrieval continues to work.

### Process Detection

- Clear process.
- Ambiguous process.
- Unknown process.
- Process change during conversation.

### Field Extraction

- New field captured.
- Existing field retained.
- Existing field updated according to existing merge rules.
- Missing field.
- Low-confidence field.
- Conflicting field.

### Context Retrieval

- Process found.
- Process not found.
- Context cached.
- Context refreshed when process changes.

### Realtime Events

- Partial transcript.
- Final transcript.
- Duplicate event.
- Out-of-order event.
- Empty event.

### End-to-End

Simulate a conversation where the customer progressively supplies required information and verify that the process and missing-field list update after each final transcript event.

---

## 20. Performance Requirements

Design for near-real-time interaction.

Avoid:

- Full conversation reprocessing on every event.
- Repeated retrieval of unchanged process context.
- Blocking operations inside Streamlit callbacks where avoidable.
- Tight polling loops.

Measure/log safely:

- Transcript event processing latency.
- Process detection latency.
- Context retrieval latency.
- Extraction latency.
- UI update latency.

Do not log sensitive transcript content unnecessarily.

---

## 21. Implementation Rules

### Reuse First

Before creating a new class/function:

1. Search the repository.
2. Identify equivalent existing functionality.
3. Reuse or extend it.
4. Only create new functionality when a genuine gap exists.

### Avoid Duplication

Do not create duplicate implementations for:

- LLM calls.
- Extraction.
- Pydantic schemas.
- Process mapping.
- Knowledge retrieval.
- Confidence calculation.
- Prompt management.
- Persistence.

### Configuration

Reuse existing configuration/secrets handling.

Do not hard-code:

- API keys.
- Endpoints.
- Model names.
- Process names.
- Field lists.
- Confidence thresholds.

---

## 22. Required Deliverables

### Analysis

```text
docs/realtime_voice_architecture.md
```

### Code

Enhance the existing repository with the minimum required changes.

Potential new components could include, only if the repository needs them:

```text
realtime/
├── transcript_events.py
├── conversation_state.py
├── realtime_processor.py
└── adapters/
    └── transcript_provider.py
```

Follow the actual repository structure instead of forcing this layout.

### UI

Enhance the existing Streamlit chat interface with:

- Conversation transcript.
- Detected process.
- Process confidence.
- Mandatory fields.
- Optional fields.
- Captured values.
- Missing fields.
- Low-confidence/conflicting fields.
- Next required information.

### Tests

Add unit and integration tests for the new realtime functionality and ensure the existing suite remains green.

### Documentation

Update `README.md` with:

- Realtime architecture.
- Configuration.
- Realtime session lifecycle.
- Transcript event format.
- Process detection.
- Context retrieval.
- Mandatory/optional field retrieval.
- Incremental extraction.
- How to run the realtime demo/UI.
- How to run tests.

---

## 23. Definition of Done

- [ ] Existing repository has been analyzed before implementation.
- [ ] `docs/realtime_voice_architecture.md` documents the existing code and enhancement plan.
- [ ] Existing extraction functionality is reused.
- [ ] Existing process/field mapping is reused.
- [ ] Existing knowledge retrieval is reused.
- [ ] Existing LangGraph state/graph is extended where appropriate.
- [ ] Realtime transcript events are supported.
- [ ] Partial/final transcript events are handled correctly.
- [ ] Conversation state is maintained per session.
- [ ] Process name can be dynamically identified from conversation.
- [ ] Process confidence is available.
- [ ] Process context can be retrieved dynamically.
- [ ] Mandatory fields are retrieved dynamically from process context.
- [ ] Optional fields are retrieved dynamically from process context.
- [ ] Fields are extracted incrementally from new conversation segments.
- [ ] Existing extracted fields are preserved/merged using repository rules.
- [ ] Missing mandatory fields are identified in near real time.
- [ ] Missing optional fields are identified separately.
- [ ] Low-confidence fields are identified.
- [ ] Conflicting values are identified.
- [ ] Process context is cached appropriately.
- [ ] Repeated LLM/context retrieval calls are minimized.
- [ ] Streamlit displays the evolving conversation.
- [ ] Streamlit displays the detected process.
- [ ] Streamlit displays mandatory and optional fields separately.
- [ ] Streamlit displays captured and missing fields.
- [ ] Streamlit displays the next required information.
- [ ] Existing functionality remains backward compatible.
- [ ] Existing tests continue to pass.
- [ ] New tests pass.
- [ ] Documentation is updated.
- [ ] No secrets or unnecessary sensitive transcript content are exposed.

---

## 24. Final Target Architecture

```text
                    CUSTOMER CALL
                         │
                         ▼
                Existing Speech-to-Text
                         │
                         ▼
              Realtime Transcript Event
                         │
                         ▼
              Existing LangGraph State
                         │
                         ▼
                 Intent Detection
                         │
                         ▼
                Process Identification
                         │
                 ┌───────┴────────┐
                 │                │
             Confident         Uncertain
                 │                │
                 ▼                ▼
          Retrieve Process     Candidate
              Context          Processes
                 │
                 ▼
        Mandatory / Optional
             Field Schema
                 │
                 ▼
        Incremental Extraction
                 │
                 ▼
        Field Status Evaluation
                 │
       ┌─────────┼─────────┐
       ▼         ▼         ▼
    Captured   Missing   Conflict/
                         Low Confidence
       │         │         │
       └─────────┼─────────┘
                 ▼
             Streamlit
             Chat UI
                 │
                 ▼
      "What information is still
       required for this process?"
```

## Core Principle

The final system must enhance the existing LangGraph project rather than becoming a second extraction platform:

```text
Existing Extraction
        +
Existing Process Mapping
        +
Existing Knowledge Retrieval
        +
Existing LangGraph
        +
Realtime Transcript Events
        +
Incremental Conversation State
        ↓
Realtime Process-Aware Customer Care Assistant
```

The system should continuously answer:

> What process is the customer asking about, what information does that process require, which required information has already been captured, and what information is still missing?

Do not proceed to downstream case creation or fulfillment in this task. The scope ends with realtime process identification, context retrieval, field tracking, and agent-facing chat context.
