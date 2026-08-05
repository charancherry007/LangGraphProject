import typer
import time
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from src.sop_orchestrator.services.project_service import ProjectService
from src.sop_orchestrator.services.skill_service import SkillService
from src.sop_orchestrator.services.knowledge_service import KnowledgeRepositoryService
from src.sop_orchestrator.runtime.session_manager import SessionManager
from src.sop_orchestrator.runtime.execution_manager import ExecutionManager
from src.sop_orchestrator.core.state import WorkflowState

app = typer.Typer()
console = Console()

PROJECTS_DIR = Path("projects")
PROJECTS_DIR.mkdir(exist_ok=True)

project_service = ProjectService(PROJECTS_DIR)
session_manager = SessionManager(project_service)

def display_header():
    console.print(Panel.fit(
        "[bold cyan]LangGraph SOP Generator[/bold cyan]",
        border_style="cyan",
        padding=(1, 5)
    ))

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        interactive_menu()

def interactive_menu():
    while True:
        display_header()
        
        console.print("1. Create Project")
        console.print("2. Open Existing Project")
        console.print("3. Settings")
        console.print("4. Exit")
        console.print()
        
        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4"], default="1")
        
        if choice == "1":
            create_project_flow()
        elif choice == "2":
            open_project_flow()
        elif choice == "3":
            console.print("[yellow]Settings not implemented in this milestone.[/yellow]")
            time.sleep(1)
        elif choice == "4":
            console.print("[green]Exiting...[/green]")
            break

def create_project_flow():
    project_name = Prompt.ask("Enter new Project Name")
    
    if (PROJECTS_DIR / project_name).exists():
        console.print(f"[red]Project '{project_name}' already exists![/red]")
        time.sleep(1)
        return
        
    try:
        project_config = session_manager.create_project(project_name)
        console.print(f"[green]Successfully created project: {project_name}[/green]")
        time.sleep(1)
        run_project_workflow(project_config)
    except Exception as e:
        console.print(f"[red]Error creating project: {str(e)}[/red]")
        time.sleep(2)

def open_project_flow():
    projects = project_service.discover_projects()
    
    if not projects:
        console.print("[yellow]No projects found. Please create one first.[/yellow]")
        time.sleep(1)
        return
        
    table = Table(title="Available Projects")
    table.add_column("No.", style="cyan", no_wrap=True)
    table.add_column("Project Name", style="magenta")
    
    for idx, name in enumerate(projects, 1):
        table.add_row(str(idx), name)
        
    console.print(table)
    
    choices = [str(i) for i in range(1, len(projects) + 1)]
    choice = Prompt.ask("Select project to open (or 0 to cancel)", choices=["0"] + choices)
    
    if choice == "0":
        return
        
    project_name = projects[int(choice) - 1]
    
    try:
        project_config = session_manager.load_project(project_name)
        run_project_workflow(project_config)
    except Exception as e:
        console.print(f"[red]Error loading project: {str(e)}[/red]")
        time.sleep(2)

def run_project_workflow(project_config):
    # Initialize execution manager
    execution_manager = ExecutionManager(project_config)
    execution_id = execution_manager.create_runtime_session()
    
    # Initialize State
    state = WorkflowState(
        project={"id": project_config.project_id, "name": project_config.project_name},
        execution_id=execution_id
    )
    
    # Validation
    console.print("\n[bold]Initializing Runtime...[/bold]")
    
    # Skills Validation
    skill_service = SkillService(project_config)
    skill_validation = skill_service.validate_skills()
    skills_ready = all(skill_validation.values())
    
    # Knowledge Validation
    knowledge_service = KnowledgeRepositoryService(project_config)
    repo_valid = knowledge_service.validate_repository()
    
    if not knowledge_service.detect_index():
        console.print("[yellow]Knowledge index not found.\nIndex will be created during Knowledge Harvesting.[/yellow]")
    
    console.print("\n[bold]Input Collection[/bold]")
    
    while True:
        l4_map = Prompt.ask("L4 Process Map path")
        path = Path(l4_map)
        if path.exists():
            state.l4_map_path = str(path)
            break
        console.print("[red]File not found. Please enter a valid path.[/red]")
        
    ref_sop = Prompt.ask("(Optional) Reference SOP path", default="")
    if ref_sop:
        path = Path(ref_sop)
        if path.exists():
            state.reference_sop_path = str(path)
        else:
            console.print("[yellow]Warning: Reference SOP not found, continuing without it.[/yellow]")
            
    docs = Prompt.ask("(Optional) Supporting Documents (comma separated paths)", default="")
    if docs:
        for doc in docs.split(","):
            path = Path(doc.strip())
            if path.exists():
                state.supporting_documents_paths.append(str(path))
            else:
                console.print(f"[yellow]Warning: Document not found: {doc.strip()}[/yellow]")
    
    # Success Screen
    console.print("\n" + "="*52)
    console.print("\n[green]Project Loaded Successfully[/green]\n")
    console.print("Execution ID")
    console.print(f"{execution_id}\n")
    
    console.print("Knowledge Repository")
    console.print("[green]READY[/green]" if repo_valid else "[red]ISSUES FOUND[/red]\n")
    
    console.print("Skills")
    console.print("[green]READY[/green]" if skills_ready else "[yellow]MISSING SKILLS[/yellow]\n")
    
    console.print("L4 Map")
    console.print("[green]READY[/green]\n")
    
    console.print("Reference SOP")
    console.print("[green]READY[/green]\n" if state.reference_sop_path else "OPTIONAL\n")
    
    console.print("Supporting Documents")
    console.print("[green]READY[/green]\n" if state.supporting_documents_paths else "OPTIONAL\n")
    
    console.print("[cyan]System Ready[/cyan]")
    console.print("Waiting for workflow execution...\n")
    console.print("="*52)
    
    # End of milestone. Pause before returning to menu or exit
    Prompt.ask("Press Enter to return to main menu")

if __name__ == "__main__":
    app()
