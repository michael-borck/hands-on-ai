#!/usr/bin/env python3

import datetime
from pathlib import Path
import markdown
import re
import json
import typer

PROJECTS_DIR = Path("docs/projects")
VERSION_FILE = Path("version.json")
OUTPUT_HTML = Path("project_browser.html")

app = typer.Typer(help="Generate HTML browser for mini-projects")

def read_markdown_files(projects_dir):
    projects = []

    for md_file in projects_dir.glob('**/*.md'):
        content = md_file.read_text(encoding='utf-8')
        
        # Match h1 titles and metadata
        title_match = re.search(r'^#\s+(.*)', content, re.MULTILINE)
        difficulty_match = re.search(r'\*\*Difficulty\*\*:\s*(.*)', content)
        focus_match = re.search(r'\*\*Learning Focus\*\*:\s*(.*)', content)
        module_match = re.search(r'\*\*Module\*\*:\s*(.*)', content)

        title = title_match.group(1).strip() if title_match else md_file.stem.replace('_', ' ').title()
        
        # Extract only the difficulty level before any hyphen
        raw_difficulty = difficulty_match.group(1).strip() if difficulty_match else 'Medium'
        difficulty = raw_difficulty.split('-')[0].strip()
        
        # Get focus areas as a comma-separated list
        focus_raw = focus_match.group(1).strip() if focus_match else 'General'
        # Split focus by commas and clean each item
        focus_areas = [area.strip() for area in focus_raw.split(',')]
        
        # Get the module type (chat, rag, agent)
        module = module_match.group(1).strip() if module_match else 'chat'
        
        # Updated line with extensions for syntax highlighting
        html_content = markdown.markdown(
            content, extensions=['fenced_code', 'codehilite']
        )

        projects.append({
            'title': title,
            'focus_raw': focus_raw,  # Keep the original string for display
            'focus_areas': focus_areas,  # List of individual focus areas
            'difficulty_raw': raw_difficulty,  # Keep the original string for display
            'difficulty': difficulty,  # Simplified difficulty for filtering
            'module': module,  # Module type for filtering
            'content': html_content
        })

    return projects

def read_local_version():
    if VERSION_FILE.exists():
        data = json.loads(VERSION_FILE.read_text())
        return data.get("version", "0.0.0")
    return "unknown"

def generate_html(projects):
    date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Extract unique focus areas from all projects
    all_focus_areas = []
    for p in projects:
        all_focus_areas.extend(p['focus_areas'])
    unique_focus_areas = sorted(set(all_focus_areas))
    
    # Get unique difficulties
    difficulties = sorted(set(p['difficulty'] for p in projects))
    
    # Get unique modules
    modules = sorted(set(p['module'] for p in projects))

    html = f"""
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Project Browser</title>
    <script src='https://cdn.tailwindcss.com'></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script>hljs.highlightAll();</script>
</head>
<body class='bg-gray-50 p-6'>
    <h1 class='text-2xl font-bold mb-4'>HandsOnAI Project Browser</h1>
    <p class='mb-4'>Generated: {date_str} v{local_version} <span id="latest-version">📁 Offline version. Visit <a href="https://github.com/michael-borck/hands-on-ai" target="_blank">HandsOnAI GitHub</a> to check for updates.</span></p>

    <div class='mb-4 flex flex-col md:flex-row gap-4'>
        <input type='text' id='search' placeholder='Search project title' class='border p-2 rounded w-full md:w-1/3'>

        <select id='moduleFilter' class='border p-2 rounded'>
            <option value='all'>All Modules</option>
            {''.join(f'<option value="{m}">{m.upper()}</option>' for m in modules)}
        </select>

        <select id='focusFilter' class='border p-2 rounded'>
            <option value='all'>All Focus Areas</option>
            {''.join(f'<option value="{f}">{f}</option>' for f in unique_focus_areas)}
        </select>

        <select id='difficultyFilter' class='border p-2 rounded'>
            <option value='all'>All Difficulties</option>
            {''.join(f'<option value="{d}">{d}</option>' for d in difficulties)}
        </select>
    </div>

    <div id='projects' class='space-y-4'>
        {''.join(generate_accordion_item(p, idx) for idx, p in enumerate(projects))}
    </div>

<script>
function toggleAccordion(idx) {{
    document.getElementById(`content-${{idx}}`).classList.toggle('hidden');
}}

const search = document.getElementById('search');
const moduleFilter = document.getElementById('moduleFilter');
const focusFilter = document.getElementById('focusFilter');
const difficultyFilter = document.getElementById('difficultyFilter');
const items = document.querySelectorAll('.project');

search.addEventListener('input', applyFilters);
moduleFilter.addEventListener('change', applyFilters);
focusFilter.addEventListener('change', applyFilters);
difficultyFilter.addEventListener('change', applyFilters);

function applyFilters() {{
    const searchVal = search.value.toLowerCase();
    const moduleVal = moduleFilter.value;
    const focusVal = focusFilter.value;
    const difficultyVal = difficultyFilter.value;

    items.forEach(item => {{
        // Fix the search functionality - search in the title 
        const matchesSearch = searchVal === '' || item.dataset.title.toLowerCase().includes(searchVal);
        
        // Check module type
        const matchesModule = moduleVal === 'all' || item.dataset.module === moduleVal;
        
        // Check if the selected focus is in the project's focus areas
        // Note: dataset attributes are camelCased in JavaScript (focusAreas) but kebab-cased in HTML (focus-areas)
        const focusAreas = JSON.parse(item.dataset.focusAreas);
        const matchesFocus = focusVal === 'all' || focusAreas.includes(focusVal);
        
        // Check difficulty
        const matchesDifficulty = difficultyVal === 'all' || item.dataset.difficulty === difficultyVal;

        item.style.display = (matchesSearch && matchesModule && matchesFocus && matchesDifficulty) ? '' : 'none';
    }});
}}
</script>
</body>
</html>
"""
    return html


def generate_accordion_item(project, idx):
    # Convert focus areas list to JSON string for the data attribute
    focus_areas_json = json.dumps(project['focus_areas'])
    
    return f"""
    <div class='project border rounded shadow-sm bg-white' 
         data-title='{project['title'].lower()}' 
         data-focus-areas='{focus_areas_json}' 
         data-difficulty='{project['difficulty']}'
         data-module='{project['module']}'>
        <button onclick='toggleAccordion({idx})' class='w-full text-left p-4 font-semibold'>
            {project['title']} <span class='text-sm text-gray-500'>({project['module'].upper()}: {project['focus_raw']} - {project['difficulty_raw']})</span>
        </button>
        <div id='content-{idx}' class='hidden p-4 border-t'>
            {project['content']}
        </div>
    </div>
"""


def build_html(projects_dir, output_path):
    projects = read_markdown_files(projects_dir)
    html = generate_html(projects)
    output_path.write_text(html, encoding='utf-8')
    return len(projects)


@app.command()
def main(
    projects_dir: Path = typer.Option(
        PROJECTS_DIR,
        "--projects-dir",
        "-p",
        help="Directory containing markdown project files",
    ),
    output: Path = typer.Option(
        OUTPUT_HTML,
        "--output",
        "-o",
        help="Output HTML file path",
    ),
):
    """Generate an HTML browser for mini-projects."""
    global local_version
    local_version = read_local_version()
    count = build_html(projects_dir, output)
    typer.echo(f"✅ Generated browser with {count} projects: {output}")


if __name__ == "__main__":
    app()