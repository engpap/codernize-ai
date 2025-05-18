import os
import click
from pathlib import Path
from rich.console import Console
from rich.progress import Progress
from openai import OpenAI
from dotenv import load_dotenv
import hashlib
import re

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
console = Console(width=200, force_terminal=True)

RELEVANT_EXTENSIONS = {
    '.java',        # Core source code: classes, controllers, services, models, etc.
    '.xml',         # Configuration files (e.g., Spring beans, persistence.xml, pom.xml)
    '.properties',  # Application settings (e.g., key-value configs for environments)
    '.yml',         # YAML configuration (e.g., Spring Boot configs)
    '.yaml',        # Same as .yml, alternate YAML extension
    '.sql',         # Database schema definitions or migration scripts
}

def scan_codebase(directory: str, debug: bool) -> list:
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if Path(filename).suffix in RELEVANT_EXTENSIONS:
                files.append(os.path.join(root, filename))
    if debug: console.print(f"[cyan]Found {len(files)} relevant files in the codebase[/cyan]")
    return files

def analyze_java_file(doc_file: str, file_path: str, debug: bool) -> str:
    """Analyze a Java file and suggest Spring Boot modernization opportunities."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": """
                You are a Java modernization expert. Analyze the provided Java file and suggest specific modernization opportunities for Spring Boot migration.
                
                For each suggestion, provide:
                1. Current Pattern: What's being used now
                2. Modern Alternative: What to use in Spring Boot
                3. Migration Steps: Step-by-step guide
                4. Benefits: Why this change is beneficial
                5. Potential Challenges: What to watch out for
                
                Format the output in Markdown with clear sections and code examples where relevant.
                Focus on:
                - Dependency Injection patterns
                - Configuration management
                - REST API implementations
                - Database access patterns
                - Security implementations
                - Testing approaches
                """},
                {"role": "user", "content": f"""
                Documentation of the project: {doc_file}
                File path: {file_path}
                
                Content:
                {content}
                """}
            ],
            temperature=0.3,
        )
        
        if debug: console.print(f"[cyan]Analysis completed for {file_path}[/cyan]")
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        console.print(f"[red]Error analyzing {file_path}: {str(e)}[/red]")
        return f"Error analyzing {file_path}: {str(e)}"

def generate_modernization_report(analyses: list, output_file: str, debug: bool):
    """Generate a combined modernization report from all analyses."""
    if debug: console.print("[blue]Generating modernization report...[/blue]")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": """
                You are a technical documentation expert. Create a comprehensive modernization report from the provided analyses.
                
                Guidelines:
                - Organize suggestions by category (e.g., DI, Security, Testing)
                - Prioritize changes based on impact and complexity
                - Include a migration roadmap
                - Add a summary of benefits and risks
                - Format in clear Markdown with proper sections
                """},
                {"role": "user", "content": "\n\n".join(analyses)}
            ],
            temperature=0.3,
        )
        
        report = response.choices[0].message.content.strip()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
            
        if debug:
            console.print(f"[green]Report generated successfully: {output_file}[/green]")
            
    except Exception as e:
        console.print(f"[red]Error generating modernization report: {str(e)}[/red]")

@click.command()
@click.argument('doc-file', required=True, default='/Users/dre/dev/interview/codernize-ai/docs/output.md', type=click.Path(exists=True))
@click.argument('repo-directory', required=True, default='/Users/dre/dev/jboss-eap-quickstarts/kitchensink', type=click.Path(exists=True))
@click.option('--output', '-o', default='docs', help='Output directory for report')
@click.option('--modernization-report-file', '-report', default='modernization-report.md', help='Output file for modernization report')
@click.option('--debug', '-d', is_flag=True, help='Enable debug output')
def main(doc_file: str, repo_directory: str, output: str, modernization_report_file: str, debug: bool):
    """Analyze Java files from documentation and suggest Spring Boot modernization opportunities."""
    if not os.getenv("OPENAI_API_KEY"):
        console.print("[red]Error: OPENAI_API_KEY environment variable not set[/red]")
        return
    
    with open(doc_file, 'r') as file:
        doc_content = file.read()

    console.print("[yellow]Extracting Java files from documentation...[/yellow]")
    java_files = scan_codebase(repo_directory, debug)
    
    if not java_files:
        console.print("[red]No Java files found in the repository[/red]")
        return
    
    analyses = []
    
    with Progress() as progress:
        task = progress.add_task("[green]Analyzing Java files...", total=len(java_files))
        
        for file_path in java_files:
            analysis = analyze_java_file(doc_content, file_path, debug)
            analyses.append(f"## Analysis for {file_path}\n\n{analysis}")
            progress.update(task, advance=1)
    
    report_path = os.path.join(output, modernization_report_file)
    generate_modernization_report(analyses, report_path, debug)

if __name__ == '__main__':
    main()
