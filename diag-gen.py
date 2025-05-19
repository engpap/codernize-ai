import os
import click
from pathlib import Path
from rich.console import Console
from rich.progress import Progress
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
console = Console(width=200, force_terminal=True)

RELEVANT_EXTENSIONS = {
    '.java',        # Core source code: classes, controllers, services, models, etc.
    '.xml',         # Configuration files (e.g., Spring beans, persistence.xml, pom.xml)
    '.sql',         # Database schema definitions or migration scripts
    '.xhtml',
    '.xml',
}

def scan_codebase(directory: str, debug: bool) -> list:
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if Path(filename).suffix in RELEVANT_EXTENSIONS:
                files.append(os.path.join(root, filename))
    if debug: console.print(f"[cyan]Found {len(files)} relevant files in the codebase[/cyan]")
    return files

def generate_file_diagram(file_path: str, debug: bool) -> str:
    """Generate a Mermaid diagram for a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": """
                You are a code analysis expert. Analyze the provided code file and generate a Mermaid diagram that shows:
                1. The main components/classes/functions
                2. Their relationships and dependencies
                3. Data flow between components
                
                Use appropriate Mermaid diagram types:
                - classDiagram for object-oriented code
                - flowchart for procedural code
                - sequenceDiagram for showing interactions
                
                Format the output as a valid Mermaid diagram with clear, concise labels.
                Focus on the most important relationships and avoid cluttering the diagram.
                 
                Return Mermaid code only.
                """},
                {"role": "user", "content": f"""
                File path: {file_path}
                
                Content:
                {content}
                """}
            ],
            temperature=0.3,
        )
        
        if debug: console.print(f"[cyan]Diagram generated for {file_path}[/cyan]")
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        console.print(f"[red]Error generating diagram for {file_path}: {str(e)}[/red]")
        return f"Error generating diagram for {file_path}: {str(e)}"

def combine_diagrams(diagrams: list, output_file: str, debug: bool):
    """Combine all individual diagrams into a comprehensive system diagram."""
    if debug: console.print("[blue]Combining diagrams into system diagram...[/blue]")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": """
                You are a system architecture expert. Create a comprehensive system diagram by combining the provided individual file diagrams.
                
                Guidelines:
                - Use a hierarchical structure to show system organization
                - Maintain clear relationships between components
                - Use appropriate Mermaid diagram types
                - Include a legend if needed
                - Keep the diagram clean and readable
                - Focus on the most important system-wide relationships
                 
                Return Mermaid code only.
                """},
                {"role": "user", "content": "\n\n".join(diagrams)}
            ],
            temperature=0.3,
        )
        
        combined_diagram = response.choices[0].message.content.strip()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(combined_diagram)
            
        if debug:
            console.print(f"[green]Combined diagram generated successfully: {output_file}[/green]")
            
    except Exception as e:
        console.print(f"[red]Error combining diagrams: {str(e)}[/red]")

def simplify_diagram(diagram_file: str, debug: bool):
    """Simplify the final diagram to keep only the most important elements."""
    if debug: console.print("[blue]Simplifying the final diagram...[/blue]")
    
    try:
        with open(diagram_file, 'r', encoding='utf-8') as f:
            diagram_content = f.read()

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": """
                You are a system architecture expert. Simplify the provided Mermaid diagram by:
                1. Keeping only the most critical components and relationships
                2. Removing redundant or less important connections
                3. Simplifying complex hierarchies while maintaining the core architecture
                4. Using clear, concise labels
                5. Ensuring the diagram remains valid Mermaid syntax
                
                Focus on making the diagram more readable while preserving the essential system structure.
                Return Mermaid code only.
                """},
                {"role": "user", "content": diagram_content}
            ],
            temperature=0.3,
        )
        
        simplified_diagram = response.choices[0].message.content.strip()
        
        # Save the simplified diagram with a new name
        simplified_file = diagram_file.replace('.mermaid', '_simplified.mermaid')
        with open(simplified_file, 'w', encoding='utf-8') as f:
            f.write(simplified_diagram)
            
        if debug:
            console.print(f"[green]Simplified diagram generated successfully: {simplified_file}[/green]")
            
    except Exception as e:
        console.print(f"[red]Error simplifying diagram: {str(e)}[/red]")

@click.command()
@click.argument('repo-directory', required=True, type=click.Path(exists=True))
@click.option('--output', '-o', default='docs', help='Output directory for diagrams')
@click.option('--combined-diagram-file', '-diagram', default='system-diagram.mermaid', help='Output file for combined diagram')
@click.option('--debug', '-d', is_flag=True, help='Enable debug output')
def main(repo_directory: str, output: str, combined_diagram_file: str, debug: bool):
    """Generate Mermaid diagrams for code files and combine them into a system diagram."""
    if not os.getenv("OPENAI_API_KEY"):
        console.print("[red]Error: OPENAI_API_KEY environment variable not set[/red]")
        return
    
    console.print("[yellow]Scanning codebase for relevant files...[/yellow]")
    files = scan_codebase(repo_directory, debug)
    
    if not files:
        console.print("[red]No relevant files found in the repository[/red]")
        return
    
    diagrams = []
    
    with Progress() as progress:
        task = progress.add_task("[green]Generating diagrams...", total=len(files))
        
        for file_path in files:
            diagram = generate_file_diagram(file_path, debug)
            diagrams.append(f"## Diagram for {file_path}\n\n```mermaid\n{diagram}\n```")
            progress.update(task, advance=1)
    
    os.makedirs(output, exist_ok=True)
    
    if debug: # Save individual diagrams
        for i, diagram in enumerate(diagrams):
            file_name = f"diagram_{i+1}.mermaid"
            with open(os.path.join(output, file_name), 'w', encoding='utf-8') as f:
                f.write(diagram)
    
    # Generate and save combined diagram
    combined_path = os.path.join(output, combined_diagram_file)
    combine_diagrams(diagrams, combined_path, debug)

    simplify_diagram(combined_path, debug)

if __name__ == '__main__':
    main()
