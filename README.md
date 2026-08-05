# LangGraph SOP Generator

L4 Process Map → SOP Generator using LangGraph and GPT-5.
This is a deterministic document engineering system where agents exchange immutable artifacts through a fixed pipeline.

## System Requirements

- Python 3.12+
- Dependencies listed in `requirements.txt` (install via `pip install -r requirements.txt`)
- OpenAI API Key (configured via environment variables or `.env` file)

## Project Configuration

Every execution belongs to a specific Project. Projects are structured as follows:

```text
project/
    knowledge/
        CHC/
        System/
        Policies/
        Templates/
        vector_store/
    skills/
        01_KnowledgeHarvesting.agent.md
        02_ProcessReconstruction.agent.md
        03_GapDiscovery.agent.md
        04_SMEInterview.agent.md
        05_L4toSOP.agent.md
        Shared/
            PromptRules.md
            ArtifactSpecification.md
            OutputFormatting.md
            CitationRules.md
            ReasoningRules.md
    inputs/
    outputs/
    reports/
    checkpoints/
    logs/
    project.yaml
```

The Knowledge folders are automatically indexed and form the primary source of truth. Skill files (`.agent.md`) act as executable specifications for each agent.

## Usage

Start the interactive CLI:

```bash
python cli.py
```

The CLI workflow follows these steps:
1. **Select Existing Project** OR **Create New Project**.
2. **Load Project**: Automatically loads Skill Specifications and the Knowledge Repository.
3. **Validate Vector Index**: The system will validate the vector store against the knowledge directory.
4. **Provide Inputs**: You will be prompted to provide:
   - L4 Process Map (Required)
   - Reference SOP (Optional)
   - Additional Supporting Documents (Optional)
5. **Run Workflow**: The fixed execution pipeline will begin.

## Execution Pipeline

The execution order is fixed and operates automatically:

1. **Knowledge Harvesting**: Extracts domain logic, rules, and actors from knowledge artifacts.
2. **Process Reconstruction**: Builds the process graph, state model, and dependencies.
3. **Gap Discovery**: Identifies assumptions, missing information, and produces a Clarification Pack.
4. **SME Interview**: Interactive CLI session where the system presents low-confidence questions to the user.
5. **SOP Generation**: Synthesizes all gathered intelligence into the final Enterprise SOP (DOCX, PDF, Markdown).

## Core Principles

- **Artifact-Driven**: Agents never communicate directly. Every agent receives artifacts and produces artifacts.
- **Single Model**: Relies exclusively on GPT-5 via `GPTService`. No model selection, fallbacks, or provider abstraction.
- **Deterministic**: The system is NOT a chatbot. It performs deterministic document engineering.
