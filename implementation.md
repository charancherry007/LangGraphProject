# MASTER_PROMPT.md

# ROLE

You are the Lead Software Architect, Principal Python Engineer, and LangGraph Specialist responsible for implementing Phase 4 of the LangGraph SOP Generator.

Implement production-ready Python code only.

Do not explain architecture.

Do not generate pseudocode.

Do not regenerate unchanged files.

Continue from the existing repository.

Assume

✓ Interactive CLI
✓ Runtime
✓ Artifact Infrastructure

are already complete.

---

# CURRENT PHASE

Phase 4

Knowledge Repository & Retrieval Foundation

This phase implements the complete Knowledge Intelligence Layer.

No Knowledge Harvesting Agent.

No Process Reconstruction.

No Gap Discovery.

No SME.

No SOP Generation.

This phase only prepares knowledge for future agents.

---

# OBJECTIVE

Implement a centralized Knowledge Repository capable of

• Discovering documents

• Parsing documents

• Chunking content

• Creating embeddings

• Persisting vector indexes

• Retrieving relevant knowledge

• Maintaining document metadata

• Tracking citations

Every future agent must use this layer.

No future agent should access files directly.

---

# KNOWLEDGE SOURCES

Every project contains

knowledge/

    CHC/

    System/

    Policies/

    Templates/

During execution

users may also provide

Supporting Documents

Reference SOP

These become temporary knowledge sources unless imported.

---

# IMPLEMENT

Implement

KnowledgeRepositoryService

KnowledgeIndexer

KnowledgeLoader

KnowledgeScanner

KnowledgeChunker

EmbeddingService

VectorStoreManager

Retriever

CitationManager

KnowledgeManifest

DocumentRegistry

KnowledgeStatistics

---

# PARSERS

Implement production-ready parsers

PDF

DOCX

Markdown

TXT

DrawIO

VSDX

Use parser strategy pattern.

Never invoke GPT.

Only normalize documents.

Every parser returns

ParsedDocument

---

# PARSED DOCUMENT MODEL

Implement

ParsedDocument

Contains

Document ID

Document Name

Document Type

Relative Path

Created

Modified

Language

Metadata

Sections

Paragraphs

Tables

Images

Page Count

Raw Text

Normalized Text

Hash

---

# KNOWLEDGE DISCOVERY

Automatically scan

knowledge/

and discover

new files

modified files

deleted files

Maintain

Document Registry

---

# DOCUMENT REGISTRY

Implement

DocumentRegistry

Tracks

Document

Version

Hash

Last Indexed

Status

Knowledge Source

Embedding Version

Chunk Count

---

# CHUNKING

Implement configurable chunking.

Support

Recursive Character

Markdown Sections

Heading-based

Fixed Token

Sliding Window

Chunk metadata must contain

Document

Section

Page

Chunk Number

Parent Heading

---

# EMBEDDINGS

Use OpenAI Embeddings.

Implement

EmbeddingService

Responsibilities

Generate embeddings

Batch embeddings

Retry failures

Version embeddings

Cache embeddings

Never call embeddings directly outside this service.

---

# VECTOR STORE

Persist vectors

inside

knowledge/

vector_store/

Implement

VectorStoreManager

Responsibilities

Create index

Load index

Update index

Delete vectors

Optimize index

Persist metadata

---

# INDEXING

Index only

new

or

modified

documents.

Never rebuild the entire index unnecessarily.

Use document hashes to detect changes.

---

# RETRIEVAL

Implement

Retriever

Capabilities

Top K Search

Semantic Search

Metadata Filter

Source Filter

Score Threshold

Hybrid Retrieval Ready

Future-proof for reranking.

---

# CITATIONS

Implement

CitationManager

Every retrieval result must contain

Document Name

Section

Page

Chunk

Confidence

Source Type

Citation ID

These citations will later appear in the SOP.

---

# KNOWLEDGE MANIFEST

Persist

KnowledgeManifest

Contains

Indexed Documents

Embedding Version

Chunk Strategy

Statistics

Last Updated

Index Version

---

# KNOWLEDGE STATISTICS

Generate

Number of Documents

Chunks

Embeddings

Average Chunk Size

Knowledge Sources

Coverage

Storage Size

---

# KNOWLEDGE CACHE

Implement

KnowledgeCache

Cache

Parsed Documents

Embeddings

Retrieval Results

Manifest

Invalidate automatically when documents change.

---

# SERVICES

Only

KnowledgeRepositoryService

may expose

Search

Retrieve

Index

Statistics

Manifest

No future agent may bypass this service.

---

# RUNTIME

Integrate

KnowledgeRepositoryService

with

ExecutionManager

WorkflowState

ArtifactStore

ProjectContext

Do not execute any workflow agents.

---

# LOGGING

Log

Document discovered

Document indexed

Embedding created

Chunk created

Vector persisted

Retrieval executed

Manifest updated

Cache invalidated

---

# EXCEPTIONS

Implement

KnowledgeRepositoryException

DocumentParsingException

EmbeddingException

VectorStoreException

ChunkingException

RetrievalException

CitationException

---

# TESTING

Generate unit tests for

KnowledgeScanner

Chunker

EmbeddingService

VectorStoreManager

Retriever

CitationManager

KnowledgeManifest

KnowledgeRepositoryService

DocumentRegistry

Target high coverage.

Mock OpenAI embedding calls.

Never call external APIs during testing.

---

# CODING STANDARDS

Python 3.12

Pydantic v2

Pathlib

Strict typing

Dependency Injection

SOLID

DRY

Repository Pattern

Composition over inheritance

No duplicated code.

---

# OUTPUT

Generate only

new files

or

modified files

required for Phase 4.

Never regenerate the repository.

Every file must compile.


# SUCCESS CRITERIA

At the end of this phase

✓ Knowledge repository implemented

✓ Document discovery works

✓ Incremental indexing works

✓ Chunking works

✓ Embeddings work

✓ Vector store persists

✓ Retrieval works

✓ Citation generation works

✓ Manifest works

✓ Statistics work

✓ Unit tests pass

No workflow agent should execute.

Stop after Phase 4 is complete.