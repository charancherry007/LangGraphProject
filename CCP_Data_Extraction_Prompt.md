# Master Prompt — LangGraph User Data Extraction, User Data Management & Core Knowledge Builder

You are an expert Python, LangGraph, LLM application, document-processing, data modeling, and Streamlit engineer.

Build a production-ready Python application that implements an AI-powered:

**User Data Extraction + User Data Repository + Process Core Knowledge Builder**

using:

- Python 3.11+
- LangGraph
- LangChain where appropriate
- GPT-5 as the primary LLM
- Streamlit
- Pydantic
- JSON-based persistence
- PyMuPDF/pdfplumber
- python-docx
- Pillow/OpenCV where required
- OCR/Vision capabilities for images
- pytest

The architecture must be modular and designed so that the same backend can later be exposed through FastAPI.

---

# 1. Primary Responsibilities

The application has THREE distinct responsibilities.

## Responsibility 1 — Extract User Data

Extract structured user information from:

- Transcription text
- PDF
- DOC/DOCX
- TXT
- PNG
- JPG/JPEG
- WEBP
- Multiple files

Return structured key-value data.

Example:

```json
{
  "first_name": "John",
  "last_name": "Smith",
  "email": "john@example.com",
  "country": "United Kingdom"
}
```

---

## Responsibility 2 — Maintain User Data JSON

The system must persist extracted user data.

The system must identify whether the extracted information belongs to:

1. An existing user
2. A completely new user

If the user already exists:

- Load the existing user JSON.
- Compare existing data with newly extracted data.
- If there is no change → IGNORE.
- If there are changes → UPDATE the existing user JSON.
- Preserve existing information that is not contradicted by the new source.
- Track what changed.

If the user is completely new:

- Create a new user JSON.

This comparison must happen **before creating a new user JSON**.

The system must never create duplicate user JSON files simply because the same user was processed again.

---

## Responsibility 3 — Maintain Process Core Knowledge

Independently create and maintain reusable process knowledge.

Core knowledge must describe:

- Fields
- Entities
- Process steps
- Business rules
- Relationships
- Terminology
- Constraints

It must NOT simply contain individual user values.

Example:

User Data:

```json
{
  "first_name": "John",
  "email": "john@example.com"
}
```

Core Knowledge:

```json
{
  "fields": [
    {
      "name": "first_name",
      "type": "string",
      "description": "First name of the customer"
    },
    {
      "name": "email",
      "type": "string",
      "description": "Email address of the customer"
    }
  ]
}
```

These two persistence mechanisms must remain separate.

---

# 2. Persistence Structure

Use the following structure:

```text
project-root/
│
├── app.py
│
├── knowledge/
│   └── core/
│       ├── customer_onboarding.json
│       └── investment_process.json
│
├── data/
│   └── users/
│       ├── john_smith.json
│       ├── jane_doe.json
│       └── ...
│
├── src/
│   ├── config/
│   ├── models/
│   ├── ingestion/
│   ├── extraction/
│   ├── users/
│   ├── knowledge/
│   ├── graph/
│   ├── services/
│   ├── utils/
│   └── ui/
│
├── tests/
│
├── requirements.txt
├── .env.example
└── README.md
```

Use:

```text
knowledge/core/
```

for reusable process knowledge.

Use:

```text
data/users/
```

for extracted user-specific data.

---

# 3. User JSON Naming

The user JSON must NOT blindly use arbitrary user-provided text as a filename.

Create a normalized unique identifier.

Preferred identification hierarchy:

```text
1. Explicit unique identifier
2. Email
3. Phone
4. Combination of stable identifying fields
5. Generated deterministic identifier
```

Example:

```json
{
  "email": "john@example.com"
}
```

could produce:

```text
data/users/john_example_com.json
```

However, do not expose sensitive data unnecessarily in filenames if a safer generated ID can be used.

Prefer:

```text
data/users/usr_8f3a7c2d.json
```

with:

```json
{
  "user_id": "usr_8f3a7c2d"
}
```

inside the JSON.

The ID generation must be deterministic when enough identifying information exists, so that the same user can be found on subsequent extractions.

---

# 4. User Identity Resolution

Create a dedicated service:

```python
UserIdentityResolver
```

with:

```python
resolve_user(extracted_data, existing_users)
```

It must determine whether the extracted information belongs to an existing user.

Example:

First extraction:

```json
{
  "name": "John Smith",
  "email": "john@example.com",
  "phone": "+441234567890"
}
```

creates:

```text
usr_123abc.json
```

Later extraction:

```json
{
  "name": "John Smith",
  "email": "john@example.com",
  "phone": "+441234567890",
  "country": "United Kingdom"
}
```

must resolve to:

```text
usr_123abc.json
```

and MUST NOT create:

```text
usr_456xyz.json
```

---

# 5. Identity Matching Strategy

Implement deterministic matching first.

Example priority:

```text
Email exact match
        ↓
Phone exact match
        ↓
Explicit user/customer ID
        ↓
Strong combination of identifying fields
```

Only use LLM-assisted identity resolution when deterministic matching cannot confidently identify the user.

If LLM matching is used:

- Require a confidence score.
- Do not merge users based on weak evidence.
- Prefer creating a reviewable ambiguous state rather than incorrectly merging two users.

Example:

```json
{
  "identity_match": {
    "status": "AMBIGUOUS",
    "candidate_user_ids": [
      "usr_123",
      "usr_456"
    ],
    "confidence": 0.62
  }
}
```

For the initial implementation, make the threshold configurable.

---

# 6. User Data JSON Schema

Create a Pydantic model.

Recommended structure:

```python
class UserData(BaseModel):
    user_id: str
    identity: dict
    attributes: dict
    metadata: dict
```

Example persisted JSON:

```json
{
  "user_id": "usr_123abc",
  "identity": {
    "name": "John Smith",
    "email": "john@example.com",
    "phone": "+441234567890"
  },
  "attributes": {
    "country": "United Kingdom",
    "occupation": "Software Engineer",
    "experience_years": 8
  },
  "metadata": {
    "created_at": "2026-09-02T10:00:00",
    "updated_at": "2026-09-02T11:30:00",
    "version": 2
  }
}
```

---

# 7. User Data Comparison

Create:

```python
compare_user_data(
    existing_data,
    extracted_data
)
```

The comparison must be deterministic.

Ignore metadata fields:

```text
created_at
updated_at
version
hash
```

when determining whether user data has changed.

Example.

Existing:

```json
{
  "name": "John Smith",
  "email": "john@example.com",
  "country": "United Kingdom"
}
```

New extraction:

```json
{
  "name": "John Smith",
  "email": "john@example.com",
  "country": "United Kingdom"
}
```

Result:

```text
UNCHANGED
```

Do not rewrite the file.

---

# 8. Updated User Data

Existing:

```json
{
  "name": "John Smith",
  "email": "john@example.com",
  "country": "United Kingdom"
}
```

New:

```json
{
  "name": "John Smith",
  "email": "john@example.com",
  "country": "United States"
}
```

Result:

```text
UPDATED
```

The persisted JSON becomes:

```json
{
  "user_id": "usr_123abc",
  "identity": {
    "name": "John Smith",
    "email": "john@example.com"
  },
  "attributes": {
    "country": "United States"
  },
  "metadata": {
    "version": 2
  }
}
```

---

# 9. User Update Rules

When updating an existing user:

### Rule 1

New information that does not exist in the old record should be added.

Example:

```text
Old:
name
email

New:
name
email
country
```

Result:

```text
name
email
country
```

### Rule 2

If an existing value has changed and the new source is reliable, update it.

Example:

```text
country:
United Kingdom → United States
```

### Rule 3

Do not replace valid information with null/empty values.

Example:

```text
Existing:
email = john@example.com

New:
email = null
```

Keep:

```text
email = john@example.com
```

### Rule 4

Preserve source/provenance information.

### Rule 5

Track changed fields.

Example:

```json
{
  "changes": [
    {
      "field": "country",
      "old_value": "United Kingdom",
      "new_value": "United States"
    }
  ]
}
```

---

# 10. Versioning

Every user JSON must contain a version.

New user:

```text
version = 1
```

Updated user:

```text
version = 2
```

No change:

```text
version remains unchanged
```

The system should not create a new physical JSON file for every version.

The current requirement is to maintain the latest version in the user's JSON.

Design the model so historical versioning can be added later.

---

# 11. User Data Hash

Create a canonical hash of user data.

Example:

```python
canonical_json = json.dumps(
    user_data,
    sort_keys=True,
    separators=(",", ":")
)

hash_value = sha256(
    canonical_json.encode()
).hexdigest()
```

Store:

```json
{
  "metadata": {
    "data_hash": "..."
  }
}
```

Use this hash to quickly determine whether extracted user data has changed.

---

# 12. User Data Operation Types

The extraction workflow must return:

```text
NEW_USER
UPDATED_USER
UNCHANGED_USER
AMBIGUOUS_USER
```

Example UI:

```text
User Data Status: UPDATED

User ID:
usr_123abc

Previous Version:
1

Current Version:
2

Changed Fields:
country
phone
```

For unchanged:

```text
User Data Status: UNCHANGED

No changes detected.
Existing user JSON was not modified.
```

For new:

```text
User Data Status: NEW_USER

Created:
data/users/usr_123abc.json
```

---

# 13. Knowledge JSON Remains Independent

The core knowledge workflow must continue independently from user data persistence.

For each process:

```text
knowledge/core/<process_key>.json
```

Example:

```text
knowledge/core/customer_onboarding.json
```

The process knowledge must be generated from the source material and reusable process concepts.

It should not contain:

```text
John Smith
john@example.com
John's phone number
```

unless those values are genuinely examples required by the process knowledge.

---

# 14. Core Knowledge Operation Types

Return:

```text
KNOWLEDGE_CREATED
KNOWLEDGE_UPDATED
KNOWLEDGE_UNCHANGED
```

Example:

```text
Knowledge Status: UPDATED

Process:
Customer Onboarding

New Knowledge:
2 fields
1 process rule
```

---

# 15. Complete LangGraph Workflow

Update the graph to:

```text
START
  │
  ▼
validate_input
  │
  ▼
ingest_sources
  │
  ▼
extract_content
  │
  ▼
extract_user_data
  │
  ▼
validate_extraction
  │
  ▼
resolve_user_identity
  │
  ├───────────────┐
  │               │
  ▼               ▼
NEW USER       EXISTING USER
  │               │
  ▼               ▼
create_user    load_user
  │               │
  │               ▼
  │          compare_user_data
  │               │
  │        ┌──────┴────────┐
  │        │               │
  │     unchanged        changed
  │        │               │
  │        ▼               ▼
  │      skip           update
  │        │               │
  └────────┴───────┬───────┘
                   │
                   ▼
          build_process_knowledge
                   │
                   ▼
          load_core_knowledge
                   │
                   ▼
          compare_knowledge
                   │
             ┌─────┴─────┐
             │           │
         unchanged      changed
             │           │
             ▼           ▼
            skip       update/create
             │           │
             └─────┬─────┘
                   │
                   ▼
                  END
```

---

# 16. LangGraph State

Use:

```python
class ExtractionState(TypedDict):
    process_name: str
    process_key: str

    transcription: str | None
    uploaded_files: list

    source_documents: list
    combined_content: str

    extracted_fields: list

    identity_result: dict

    user_id: str | None

    existing_user_data: dict | None
    new_user_data: dict | None

    user_data_operation: str
    user_data_changes: list

    existing_knowledge: dict | None
    knowledge_candidate: dict | None

    knowledge_operation: str
    knowledge_changes: list

    errors: list
```

---

# 17. Repository Services

Create separate repositories.

## UserRepository

```python
class UserRepository:
    def find_by_identity(...)
    def get_user(...)
    def create_user(...)
    def update_user(...)
    def list_users(...)
```

## KnowledgeRepository

```python
class KnowledgeRepository:
    def get_process_knowledge(...)
    def create_knowledge(...)
    def update_knowledge(...)
    def compare_knowledge(...)
```

Do not mix user persistence and knowledge persistence.

---

# 18. User Repository Search

Because there may eventually be thousands of user JSON files, do not scan and parse every JSON file for every request if it can be avoided.

Create an identity index.

Example:

```text
data/
├── users/
│   ├── usr_123.json
│   ├── usr_456.json
│
└── index/
    └── user_identity_index.json
```

Example:

```json
{
  "email:john@example.com": "usr_123",
  "phone:+441234567890": "usr_123"
}
```

When a new user is created, update the index.

When user identity changes, update the index.

Use atomic writes.

The index is an optimization and the user JSON remains the source of truth.

---

# 19. Multiple Sources

If the same extraction contains:

```text
transcription
+
customer_form.pdf
+
customer_image.png
```

combine the extracted information.

Example:

Transcription:

```text
John Smith lives in London.
```

PDF:

```text
Email: john@example.com
```

Image:

```text
Phone: +441234567890
```

Final user data:

```json
{
  "name": "John Smith",
  "location": "London",
  "email": "john@example.com",
  "phone": "+441234567890"
}
```

Track provenance for each field.

---

# 20. Conflict Resolution

If multiple sources provide different values:

```text
PDF:
country = United Kingdom

Image:
country = United States
```

Do not silently choose a value without a defined strategy.

Implement source-aware conflict resolution.

Preferred approach:

1. Determine source reliability.
2. Prefer explicit/latest information when supported.
3. If ambiguity remains, surface the conflict.

Example:

```json
{
  "field": "country",
  "conflict": true,
  "values": [
    {
      "value": "United Kingdom",
      "source": "form.pdf"
    },
    {
      "value": "United States",
      "source": "profile.png"
    }
  ]
}
```

The UI should show a warning when conflicts occur.

---

# 21. Streamlit UI

Create a clean UI with:

```text
==============================================
 AI User Data Extraction & Knowledge Builder
==============================================

Process Name
[ Customer Onboarding ]

User Identifier (Optional)
[____________________________]

Transcription
┌────────────────────────────────────────────┐
│ Paste transcription here                   │
│                                            │
│                                            │
└────────────────────────────────────────────┘

Upload Files
[ Choose files ]

Supported:
PDF | DOCX | TXT | PNG | JPG | WEBP

[ Start Extraction ]
```

The optional User Identifier can be used when the source contains a known external ID.

---

# 22. Extraction Results UI

Display:

```text
User Data
```

as:

| Key | Value | Source | Confidence |
|---|---|---|---|
| first_name | John | transcription | 0.98 |
| last_name | Smith | transcription | 0.98 |
| email | john@example.com | form.pdf | 0.99 |

---

# 23. User Data Status UI

Display a dedicated section:

```text
User Data Status
```

Possible:

### New

```text
🟢 NEW USER

User ID:
usr_123abc

Version:
1

Action:
Created new user JSON
```

### Updated

```text
🟡 USER UPDATED

User ID:
usr_123abc

Previous Version:
1

Current Version:
2

Changed Fields:
- country
- phone
```

### Unchanged

```text
🔵 NO USER DATA CHANGES

User ID:
usr_123abc

Existing version:
2

Action:
No file update required
```

### Ambiguous

```text
🔴 AMBIGUOUS USER

Multiple existing users may match this data.

Do not automatically merge.
```

---

# 24. Knowledge Status UI

Display separately:

```text
Core Knowledge Status
```

Example:

```text
Process:
Customer Onboarding

Operation:
UPDATED

Knowledge File:
knowledge/core/customer_onboarding.json

Version:
3

New Knowledge:
2
```

This makes it immediately clear that:

**User Data Status ≠ Knowledge Status**

---

# 25. Multi-Session Support

Streamlit must support multiple concurrent sessions.

Use:

```python
st.session_state
```

for session-specific data.

Never store user-specific extraction results in global mutable variables.

Each session must maintain:

```text
process_name
transcription
uploaded_files
extraction_results
user_data_status
knowledge_status
errors
```

The repositories are shared across sessions.

Therefore implement safe concurrent persistence using:

- Atomic file writes
- File locking where appropriate
- Read-before-write
- Conflict detection
- Retry where appropriate

---

# 26. Atomic JSON Writes

Never directly overwrite JSON files.

Use:

```text
write temporary file
        ↓
flush
        ↓
replace target file atomically
```

For example:

```python
temp_file = target.with_suffix(".tmp")

temp_file.write_text(...)

temp_file.replace(target)
```

Ensure the application cannot leave corrupted JSON after an interrupted write.

---

# 27. User Data Merge Algorithm

Implement:

```python
merge_user_data(
    existing_user,
    extracted_user
)
```

Algorithm:

```text
For every extracted field:

    if field doesn't exist:
        add field

    elif extracted value is null:
        preserve existing value

    elif values are equal:
        preserve existing value

    elif new value is trustworthy:
        update existing value
        record change

    else:
        record conflict
```

Return:

```python
{
    "merged_data": {...},
    "changes": [...],
    "conflicts": [...]
}
```

---

# 28. Knowledge Merge Algorithm

Implement:

```python
merge_knowledge(
    existing_knowledge,
    candidate_knowledge
)
```

Rules:

- Add new fields.
- Add new entities.
- Add new process steps.
- Add new rules.
- Add new relationships.
- Merge compatible descriptions.
- Avoid duplicates.
- Preserve provenance.
- Never remove existing knowledge.
- Ignore individual user-specific values.

---

# 29. Important Idempotency Requirement

The workflow must be idempotent.

Running the exact same input multiple times must NOT continuously modify files.

Example:

```text
Run 1:
NEW USER
User version = 1

Run 2:
UNCHANGED USER
User version = 1

Run 3:
UNCHANGED USER
User version = 1
```

Similarly:

```text
Knowledge Run 1:
CREATED
version = 1

Knowledge Run 2:
UNCHANGED
version = 1

Knowledge Run 3:
UNCHANGED
version = 1
```

Only genuinely new/changed information should cause an update.

---

# 30. Complete Workflow Result

Return:

```python
class WorkflowResult(BaseModel):
    process_name: str
    process_key: str

    extracted_fields: list[ExtractedField]

    user_id: str | None

    user_operation: Literal[
        "NEW_USER",
        "UPDATED_USER",
        "UNCHANGED_USER",
        "AMBIGUOUS_USER"
    ]

    user_version: int | None

    user_changes: list

    knowledge_operation: Literal[
        "KNOWLEDGE_CREATED",
        "KNOWLEDGE_UPDATED",
        "KNOWLEDGE_UNCHANGED"
    ]

    knowledge_version: int | None

    knowledge_changes: list

    errors: list[str]
```

---

# 31. Example Scenario — New User

Input:

```text
Process:
Customer Onboarding

Transcription:
My name is John Smith.
My email is john@example.com.
I live in London.
```

Result:

```text
User:
NEW_USER

User ID:
usr_123abc

Version:
1
```

Create:

```text
data/users/usr_123abc.json
```

If process knowledge doesn't exist:

```text
knowledge/core/customer_onboarding.json
```

is created.

---

# 32. Example Scenario — Same User, Same Data

Input again:

```text
My name is John Smith.
My email is john@example.com.
I live in London.
```

Result:

```text
User:
UNCHANGED_USER

Version:
1
```

No rewrite.

Knowledge:

```text
KNOWLEDGE_UNCHANGED
```

No rewrite.

---

# 33. Example Scenario — Same User, Updated Data

Existing:

```json
{
  "name": "John Smith",
  "email": "john@example.com",
  "location": "London"
}
```

New source:

```text
John Smith has moved to Manchester.
```

Result:

```text
User:
UPDATED_USER

Previous Version:
1

Current Version:
2

Changes:
location:
London → Manchester
```

Update:

```text
data/users/usr_123abc.json
```

Do NOT create a new user file.

---

# 34. Example Scenario — Same User, New Information

Existing:

```json
{
  "name": "John Smith",
  "email": "john@example.com"
}
```

New source:

```text
John Smith lives in London and works as a Software Engineer.
```

Result:

```text
UPDATED_USER
```

Merged:

```json
{
  "name": "John Smith",
  "email": "john@example.com",
  "location": "London",
  "occupation": "Software Engineer"
}
```

Version increments.

---

# 35. Example Scenario — Completely New User

Input:

```text
Jane Doe
jane@example.com
Lives in Birmingham
```

If identity matching finds no existing user:

```text
NEW_USER
```

Create:

```text
data/users/usr_new_id.json
```

Version:

```text
1
```

---

# 36. Example Scenario — Same User, Conflicting Sources

Input:

```text
PDF:
John Smith
Country: UK

Image:
John Smith
Country: USA
```

The system should not silently overwrite the value.

Return:

```text
AMBIGUOUS / CONFLICT
```

and display:

```text
Country conflict detected:

UK  → form.pdf
USA → profile.png
```

The conflict should be included in the workflow result.

---

# 37. GPT-5 Extraction Prompt

Create a dedicated prompt:

```text
You are an expert structured data extraction agent.

Extract all meaningful user/customer/person information from the supplied sources.

Requirements:

1. Extract only information supported by the sources.
2. Never hallucinate values.
3. Infer reasonable field names.
4. Preserve nested structures.
5. Preserve arrays when multiple values exist.
6. Identify stable identity attributes.
7. Identify possible unique identifiers.
8. Assign confidence between 0 and 1.
9. Preserve source provenance.
10. Detect conflicting values across sources.
11. Do not generate process knowledge.
12. Do not invent missing information.

Return structured data matching the Pydantic schema.
```

---

# 38. GPT-5 Knowledge Prompt

Create a separate prompt:

```text
You are an expert process knowledge extraction agent.

Analyze the supplied source material and identify reusable knowledge about the specified process.

Extract:

- Entities
- Fields
- Field definitions
- Process steps
- Business rules
- Relationships
- Constraints
- Terminology

Important:

1. Only use information supported by the source.
2. Do not hallucinate.
3. Do not store individual user values as process knowledge.
4. Extract reusable concepts.
5. Preserve source provenance.
6. Merge naturally with existing process knowledge.
7. Avoid duplicates.
8. Return structured JSON.
```

---

# 39. Project Structure

Use:

```text
project-root/
│
├── app.py
├── requirements.txt
├── .env.example
├── README.md
│
├── knowledge/
│   └── core/
│
├── data/
│   ├── users/
│   └── index/
│
├── src/
│   ├── config/
│   │   └── settings.py
│   │
│   ├── models/
│   │   ├── extraction_models.py
│   │   ├── user_models.py
│   │   ├── knowledge_models.py
│   │   └── workflow_models.py
│   │
│   ├── ingestion/
│   │   ├── text_loader.py
│   │   ├── pdf_loader.py
│   │   ├── docx_loader.py
│   │   ├── image_loader.py
│   │   └── file_router.py
│   │
│   ├── extraction/
│   │   ├── user_data_extractor.py
│   │   ├── knowledge_extractor.py
│   │   └── validators.py
│   │
│   ├── users/
│   │   ├── identity_resolver.py
│   │   ├── user_comparator.py
│   │   ├── user_merger.py
│   │   ├── user_repository.py
│   │   └── identity_index.py
│   │
│   ├── knowledge/
│   │   ├── knowledge_builder.py
│   │   ├── knowledge_comparator.py
│   │   ├── knowledge_merger.py
│   │   └── knowledge_repository.py
│   │
│   ├── graph/
│   │   ├── state.py
│   │   ├── nodes.py
│   │   └── workflow.py
│   │
│   ├── services/
│   │   └── extraction_service.py
│   │
│   ├── utils/
│   │   ├── hashing.py
│   │   ├── json_utils.py
│   │   ├── file_utils.py
│   │   └── logging_utils.py
│   │
│   └── ui/
│       ├── extraction_view.py
│       └── session_manager.py
│
└── tests/
```

---

# 40. Testing Requirements

Create tests for:

## User Identity

```text
existing email → same user
existing phone → same user
new email → new user
ambiguous identity → ambiguous
```

## User Comparison

```text
same data → unchanged
new field → updated
changed field → updated
null new field → unchanged
```

## User Merge

```text
new fields are added
changed fields are updated
existing fields are preserved
duplicates aren't created
```

## Knowledge

```text
same knowledge → unchanged
new knowledge → updated
new process → created
```

## Idempotency

Run the same extraction multiple times.

Verify:

```text
User version does not increase unnecessarily.
Knowledge version does not increase unnecessarily.
No duplicate JSON files are created.
```

## Concurrency

Test concurrent repository access where practical.

---

# 41. Final Acceptance Criteria

The project is complete only when all of the following work:

```text
[ ] Streamlit application starts
[ ] Multiple Streamlit sessions are supported
[ ] Process name is supported
[ ] Optional external user identifier is supported
[ ] Transcription input works
[ ] Multiple file uploads work
[ ] TXT works
[ ] PDF works
[ ] DOCX works
[ ] Images work
[ ] GPT-5 extraction works
[ ] Structured Pydantic extraction works
[ ] User identity resolution works
[ ] New user JSON is created
[ ] Existing user JSON is detected
[ ] Same user + same data = IGNORE
[ ] Same user + new data = UPDATE
[ ] Same user + changed data = UPDATE
[ ] Null values don't overwrite valid data
[ ] Conflicts are detected
[ ] User versioning works
[ ] User hash comparison works
[ ] No duplicate users are created
[ ] Identity index works
[ ] Core knowledge JSON is created
[ ] Existing core knowledge is detected
[ ] Same knowledge = SKIP
[ ] New knowledge = UPDATE
[ ] Knowledge is additive
[ ] Duplicate knowledge is prevented
[ ] User data and knowledge remain separate
[ ] Source provenance is maintained
[ ] Atomic writes are implemented
[ ] Errors are handled
[ ] Logging is implemented
[ ] Secrets are protected
[ ] Unit tests are implemented
[ ] README is complete
```

---

# 42. Most Important Design Principle

The implementation MUST maintain a strict separation:

```text
┌─────────────────────────────────────────────┐
│                 INPUT SOURCES                │
│                                             │
│ Transcript | PDF | DOCX | TXT | Image      │
└───────────────────┬─────────────────────────┘
                    │
                    ▼
          ┌─────────────────────┐
          │  AI EXTRACTION      │
          └──────────┬──────────┘
                     │
          ┌──────────┴───────────┐
          │                      │
          ▼                      ▼
┌───────────────────┐   ┌────────────────────┐
│   USER DATA       │   │ PROCESS KNOWLEDGE  │
│                   │   │                    │
│ Actual values     │   │ Reusable concepts  │
│ User identity     │   │ Fields             │
│ Attributes        │   │ Rules              │
│ User history      │   │ Steps              │
└─────────┬─────────┘   │ Entities           │
          │             └──────────┬─────────┘
          ▼                        ▼
 data/users/                 knowledge/core/
```

The **User Data Repository answers:**

> "What do we know about this specific user?"

The **Core Knowledge Repository answers:**

> "What do we know about this process?"

Do not mix these responsibilities.

The resulting architecture must be suitable for future agents that consume:

```text
data/users/*.json
```

for user-specific context and:

```text
knowledge/core/*.json
```

for reusable process knowledge.