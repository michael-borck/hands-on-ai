#!/usr/bin/env python3

"""
Generate a project index file for the docs/projects directory.

This script scans the projects directory and generates an index.md file
that lists all projects by category.
"""

import os
from pathlib import Path
import re
import typer

app = typer.Typer(help="Generate a project index file")

def extract_title(file_path):
    """Extract the title from a markdown file (first h1 heading)."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for the first # heading
            match = re.search(r'^# (.+)$', content, re.MULTILINE)
            if match:
                return match.group(1)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    # If no title found, use the filename
    return Path(file_path).stem.replace('-', ' ').title()

@app.callback(invoke_without_command=True)
def main(
    projects_dir: str = typer.Option(
        "docs/projects", 
        "--dir", 
        "-d", 
        help="Path to the projects directory"
    ),
    output_file: str = typer.Option(
        "docs/projects/index.md",
        "--output",
        "-o",
        help="Path to the output index file"
    )
):
    """Generate a project index file."""
    projects_path = Path(projects_dir)
    output_path = Path(output_file)
    
    if not projects_path.is_dir():
        typer.echo(f"Error: Directory '{projects_path}' does not exist.")
        raise typer.Exit(code=1)
    
    # Get subdirectories (categories)
    categories = [d for d in projects_path.iterdir() if d.is_dir()]
    
    # Prepare the content
    content = ["# Project Gallery\n", 
               "This page lists all the mini-projects available in Hands-On AI, organized by module.\n"]
    
    # Sort categories
    category_order = {"chat": 1, "rag": 2, "agent": 3}
    categories.sort(key=lambda x: category_order.get(x.name.lower(), 999))
    
    for category in categories:
        category_name = category.name.title()
        
        # Add descriptions based on category
        if category_name.lower() == "chat":
            description = "Chat mini-projects focus on using LLMs for conversational interactions."
        elif category_name.lower() == "rag":
            description = "RAG (Retrieval-Augmented Generation) projects focus on combining document retrieval with LLM generation."
        elif category_name.lower() == "agent":
            description = "Agent projects focus on LLMs that can use tools and follow a reasoning process."
        else:
            description = f"{category_name} projects for Hands-On AI."
        
        content.append(f"## {category_name} Projects\n")
        content.append(f"{description}\n")
        
        # Get markdown files in this category
        project_files = sorted([
            f for f in category.glob("*.md") 
            if f.is_file() and f.name != "index.md"
        ])
        
        for project_file in project_files:
            title = extract_title(project_file)
            rel_path = project_file.relative_to(projects_path)
            content.append(f"- [{title}]({rel_path})")
        
        content.append("")  # Add a blank line between categories
    
    # Write the index file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(content))
    
    typer.echo(f"✅ Generated project index at {output_path}")

if __name__ == "__main__":
    app()
