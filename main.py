import os
import click
from pathlib import Path
from rich.console import Console
from rich.progress import Progress
from openai import OpenAI
from dotenv import load_dotenv
import hashlib

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
    '.md',          # Markdown documentation (README, CONTRIBUTING, etc.)
    '.adoc'         # AsciiDoc documentation files (project guides, architecture docs_v0)
}

VALID_CATEGORIES = {
    'API',
    'Data Model',
    'Business Logic',
    'Persistence',
    'Configuration',
    'Security',
    'Testing',
    'Utilities',
    'Documentation',
    'Other'
}
def scan_codebase(directory: str) -> list:
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if Path(filename).suffix in RELEVANT_EXTENSIONS:
                files.append(os.path.join(root, filename))
    # console.print(f"[cyan]Found {len(files)} relevant files in the codebase[/cyan]")
    return files


def categorize_file(file_path: str, file_content: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content":
                    """
                    - API: REST controllers, routes, request handlers
                    - Data Model: Entity classes, value objects, enums
                    - Business Logic: Core services, domain logic, use case implementation
                    - Persistence: Repositories, DAOs, database interaction code
                    - Configuration: Spring Boot/Jakarta EE configuration and setup classes
                    - Security: Authentication, authorization, filters, tokens
                    - Testing: Unit tests, integration tests, mocks, test helpers
                    - Utilities: Common helper methods, constants, exceptions
                    - Documentation: Markdown, AsciiDoc, comments, usage guides
                    - Other: Everything else

                    Respond with ONLY the category name, nothing else.
                    """},

                {"role": "user", "content":
                    f"""
                    File path: {file_path}
                    
                    Content:
                    {file_content}
                    """
                }
            ],
            temperature=0.3,
        )
        category = response.choices[0].message.content.strip()
        # console.print(f"[cyan]Category for {file_path}: {category}[/cyan]")
        return category if category in VALID_CATEGORIES else 'Other'
    except Exception as e:
        console.print(f"[red]Error categorizing {file_path}: {str(e)}[/red]")
        return 'Other'


def generate_short_doc(file_path: str, file_content: str, category: str) -> str:
    if category in ["API", "Data Model", "Business Logic"]:
        sys_prompt = """
            You are a documentation expert. Given a file and its category, generate a Markdown section documentation describing the file.
            
            Guidelines:
            - Focus only on public-facing parts (e.g., method names, class signatures, config sections);
            - DO NOT INCLUDE CODE IMPLEMENTATION.
            - Be structured and schematic.
            - Write only Markdown output.
                
            Example Output:
            ```
            torch.zeros
            torch.zeros(*size, *, out=None, dtype=None, layout=torch.strided, device=None, requires_grad=False) → Tensor
            Returns a tensor filled with the scalar value 0, with the shape defined by the variable argument size.
            
            Parameters
            size (int...) – a sequence of integers defining the shape of the output tensor. Can be a variable number of arguments or a collection like a list or tuple.
            
            Keyword Arguments
            out (Tensor, optional) – the output tensor.
            
            dtype (torch.dtype, optional) – the desired data type of returned tensor. Default: if None, uses a global default (see torch.set_default_dtype()).
            
            layout (torch.layout, optional) – the desired layout of returned Tensor. Default: torch.strided.
            
            device (torch.device, optional) – the desired device of returned tensor. Default: if None, uses the current device for the default tensor type (see torch.set_default_device()). device will be the CPU for CPU tensor types and the current CUDA device for CUDA tensor types.
            
            requires_grad (bool, optional) – If autograd should record operations on the returned tensor. Default: False.
            ```
        """
    else:
        sys_prompt = """
        You are a documentation expert. Given a file and its category, generate a short Markdown section summarizing the file.
        
        Guidelines:
        - Focus only on public-facing parts (e.g., method names, class signatures, config sections); DO NOT INCLUDE CODE IMPLEMENTATION.
        - Keep it short and clear.
        - Be structured and schematic.
        - Write only Markdown output.
        """
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content":
                    f"""
                    File path: {file_path}
                    Category: {category}

                    Content:
                    {file_content}
                    """
                }
            ],
            temperature=0.3,
        )
        console.print(f"[cyan]Short doc generated for {file_path}[/cyan]")
        return response.choices[0].message.content.strip()
    except Exception as e:
        console.print(f"[red]Error documenting {file_path}: {str(e)}[/red]")
        return f"// Error documenting {file_path}"


def generate_initial_documentation() -> str:
    return """= Project Documentation

== Overview
This document provides comprehensive documentation for the project, organized by different components and aspects.

"""

def generate_combined_documentation_summary(short_docs: list[str]) -> str:
    """Use GPT to summarize and structure the documentation from combined short docs."""
    console.print("[blue]Generating a documentation summary from all short docs...[/blue]")
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Or other reasoning models
            messages=[
                {"role": "system", "content": """
                Given a list of small documentation snippets of a project, combine them into a single big documentation file.
                
                Guidelines:
                - Write only Markdown output.
                - Be structured and schematic.
                - Reserve all technical detail—add nothing, omit nothing.
                """},
                {"role": "user", "content": "\n\n".join(short_docs)}
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        console.print(f"[red]Error generating combined documentation summary: {str(e)}[/red]")
        return "\n\n".join(short_docs)


def hash_content(content: str) -> str:
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def clean_up_documentation(raw_doc: str) -> str:
    """Use GPT to clean up and format the final Markdown content."""
    console.print("[blue]Running final cleanup on documentation...[/blue]")
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Or other reasoning models
            messages=[
                {"role": "system", "content": """
                Given a Markdown document that serves as a project’s documentation, re-organize its content to improve the overall structure, sectioning, and flow.
                Your goal is to make the document more logically organized, readable, and suitable for publication.
                
                - Write only Markdown output.
                - Do not remove any information.
                """},
                {"role": "user", "content": f"""Here is the generated documentation:
                {raw_doc}
                """}
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        console.print(f"[red]Error cleaning up final documentation: {str(e)}[/red]")
        return raw_doc  # Fallback to raw if something fails

@click.command()
@click.argument('directory', required=False, default='/Users/dre/dev/jboss-eap-quickstarts/kitchensink', type=click.Path(exists=True))
@click.option('--output', '-o', default='docs', help='Output directory for documentation')
@click.option('--doc-file', '-d', default='project.md', help='Name of the documentation file')
def main(directory: str, output: str, doc_file: str):
    """Generate and maintain documentation for a codebase."""
    if not os.getenv("OPENAI_API_KEY"):
        console.print("[red]Error: OPENAI_API_KEY environment variable not set[/red]")
        return

    debug_dir = os.path.join(output, "debug")
    short_doc_dir = os.path.join(debug_dir, "short_docs")
    os.makedirs(short_doc_dir, exist_ok=True)

    os.makedirs(output, exist_ok=True)
    doc_path = os.path.join(output, doc_file)

    base_doc = generate_initial_documentation()
    short_docs = []

    console.print("[yellow]Scanning codebase...[/yellow]")
    files = scan_codebase(directory)

    if not files:
        console.print("[red]No relevant files found in the specified directory[/red]")
        return

    with Progress() as progress:
        total_steps = len(files) + 2  # +1 for combination, +1 for cleanup
        task = progress.add_task("[green]Processing documentation steps...", total=total_steps)

        # Step 1: Short doc generation per file
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                category = categorize_file(file_path, content)
                short_doc = generate_short_doc(file_path, content, category)

                # Save short doc for debugging
                short_doc_filename = hash_content(file_path) + "_short.md"
                with open(os.path.join(short_doc_dir, short_doc_filename), 'w', encoding='utf-8') as f:
                    f.write(short_doc)

                short_docs.append(short_doc)
                progress.update(task, advance=1)

            except Exception as e:
                console.print(f"[red]Error processing {file_path}: {str(e)}[/red]")
                progress.update(task, advance=1)  # Still advance to not block progress bar
                continue

        # Step 2: Combine documentation
        combined_doc = generate_combined_documentation_summary(short_docs)
        raw_doc_debug_path = os.path.join(debug_dir, 'raw_' + doc_file)
        with open(raw_doc_debug_path, 'w', encoding='utf-8') as f:
            f.write(combined_doc)
        progress.update(task, advance=1)

        # Step 3: Clean up final doc
        cleaned_doc = clean_up_documentation(combined_doc)
        with open(doc_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_doc)
        progress.update(task, advance=1)

    console.print(f"[green]Documentation saved to '{doc_path}'[/green]")

if __name__ == '__main__':
    main()