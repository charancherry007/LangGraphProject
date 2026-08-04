import typer
from rich.console import Console
app=typer.Typer()
console=Console()

@app.command()
def run():
    console.print("[bold green]LangGraph SOP Generator[/bold green]")
    console.print("Bootstrap complete. Next phases will add workflow.")

if __name__=="__main__":
    app()
