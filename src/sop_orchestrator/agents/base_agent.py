from abc import ABC, abstractmethod
from typing import Dict, Any
from src.sop_orchestrator.core.state import WorkflowState

class BaseAgent(ABC):
    def __init__(self, agent_name: str):
        self.agent_name = agent_name

    @abstractmethod
    def collect_context(self, state: WorkflowState) -> Dict[str, Any]:
        """Collect necessary context for the agent's execution."""
        pass

    @abstractmethod
    def build_prompt(self, context: Dict[str, Any], skill_spec: str) -> str:
        """Construct the prompt based on context and skill specification."""
        pass

    @abstractmethod
    def execute(self, state: WorkflowState) -> WorkflowState:
        """Execute the agent's core logic and return updated state."""
        pass

    @abstractmethod
    def validate(self, output: Dict[str, Any]) -> bool:
        """Validate the generated output."""
        pass

    @abstractmethod
    def post_process(self, output: Dict[str, Any], state: WorkflowState) -> WorkflowState:
        """Process the validated output into final artifacts and update state."""
        pass
