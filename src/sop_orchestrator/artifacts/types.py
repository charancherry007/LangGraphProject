from typing import Dict, Any, List
from pydantic import Field
from src.sop_orchestrator.artifacts.base import BaseArtifact

# --- Knowledge Artifacts ---
class KnowledgePackage(BaseArtifact):
    domain_knowledge: str = ""

class EvidenceGraph(BaseArtifact):
    nodes: List[Dict[str, Any]] = Field(default_factory=list)
    edges: List[Dict[str, Any]] = Field(default_factory=list)

class ArtifactCatalog(BaseArtifact):
    catalog: Dict[str, Any] = Field(default_factory=dict)

class BusinessRules(BaseArtifact):
    rules: List[str] = Field(default_factory=list)

class Glossary(BaseArtifact):
    terms: Dict[str, str] = Field(default_factory=dict)

class ActorCatalog(BaseArtifact):
    actors: List[str] = Field(default_factory=list)

class SystemCatalog(BaseArtifact):
    systems: List[str] = Field(default_factory=list)

# --- Process Artifacts ---
class ProcessGraph(BaseArtifact):
    nodes: List[Dict[str, Any]] = Field(default_factory=list)
    edges: List[Dict[str, Any]] = Field(default_factory=list)

class DecisionInventory(BaseArtifact):
    decisions: List[Dict[str, Any]] = Field(default_factory=list)

class StateModel(BaseArtifact):
    states: List[str] = Field(default_factory=list)
    transitions: List[Dict[str, Any]] = Field(default_factory=list)

class ProcessVariants(BaseArtifact):
    variants: List[Dict[str, Any]] = Field(default_factory=list)

# --- Gap Artifacts ---
class GapRegister(BaseArtifact):
    gaps: List[Dict[str, Any]] = Field(default_factory=list)

class ClarificationPack(BaseArtifact):
    clarifications: List[Dict[str, Any]] = Field(default_factory=list)

class ConfidenceDashboard(BaseArtifact):
    metrics: Dict[str, float] = Field(default_factory=dict)

class Assumptions(BaseArtifact):
    assumptions_list: List[str] = Field(default_factory=list)

class RiskRegister(BaseArtifact):
    risks: List[Dict[str, Any]] = Field(default_factory=list)

# --- SME Artifacts ---
class QuestionBank(BaseArtifact):
    questions: List[Dict[str, Any]] = Field(default_factory=list)

class ValidatedAnswers(BaseArtifact):
    answers: List[Dict[str, Any]] = Field(default_factory=list)

class DecisionLog(BaseArtifact):
    logs: List[Dict[str, Any]] = Field(default_factory=list)

# --- SOP Artifacts ---
class EnterpriseSOP(BaseArtifact):
    content_markdown: str = ""

class TraceabilityMatrix(BaseArtifact):
    matrix: List[Dict[str, Any]] = Field(default_factory=list)

class ExecutionReport(BaseArtifact):
    report: str = ""
