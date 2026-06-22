"""
Index command for the rag CLI - creates vector indices from document files.
"""

import typer
from rich import print
from pathlib import Path
import os
import time
from ...config import CONFIG_DIR, get_chunk_size, log
from ..utils import load_text_file, chunk_text, get_embeddings, save_index_with_sources

app = typer.Typer(help="Build a RAG index from files")


@app.callback(invoke_without_command=True)
def index(
    input_path: str = typer.Argument(..., help="File or directory to index"),
    output_file: str = typer.Option(None, help="Output index file (default: ~/.hands-on-ai/index.npz)"),
    chunk_size: int = typer.Option(None, help="Words per chunk (default: from config)"),
    force: bool = typer.Option(False, help="Overwrite existing index"),
):
    """Build a RAG index from files."""
    # Determine the output path
    if output_file is None:
        CONFIG_DIR.mkdir(exist_ok=True)
        output_file = str(CONFIG_DIR / "index.npz")
    
    # Check if output file already exists
    if os.path.exists(output_file) and not force:
        print(f"[yellow]⚠️ Index file {output_file} already exists. Use --force to overwrite.[/yellow]")
        raise typer.Exit(1)
    
    # Get default chunk size from config if not specified
    if chunk_size is None:
        chunk_size = get_chunk_size()
    
    # Process the input file(s)
    path = Path(input_path)
    if not path.exists():
        print(f"[red]❌ Path not found: {path}[/red]")
        raise typer.Exit(1)
    
    start_time = time.time()
    chunks = []
    sources = []
    
    # Process a single file
    if path.is_file():
        print(f"📄 Loading file: {path}")
        try:
            text = load_text_file(path)
            file_chunks = chunk_text(text, chunk_size)
            chunks.extend(file_chunks)
            sources.extend([str(path)] * len(file_chunks))
            print(f"  ✓ Generated {len(file_chunks)} chunks")
        except Exception as e:
            print(f"[red]❌ Error processing {path}: {e}[/red]")
    
    # Process a directory of files
    elif path.is_dir():
        print(f"📂 Processing directory: {path}")

        # Find all supported files
        supported_extensions = [".txt", ".md", ".docx", ".pdf"]
        files: list[Path] = []
        for ext in supported_extensions:
            files.extend(path.glob(f"**/*{ext}"))

        if not files:
            print(f"[yellow]⚠️ No supported files found in {path}[/yellow]")
            raise typer.Exit(1)
        
        # Process each file
        print(f"Found {len(files)} files to process")
        for i, file_path in enumerate(files):
            try:
                print(f"[{i+1}/{len(files)}] Processing: {file_path}")
                text = load_text_file(file_path)
                file_chunks = chunk_text(text, chunk_size)
                chunks.extend(file_chunks)
                sources.extend([str(file_path)] * len(file_chunks))
                print(f"  ✓ Generated {len(file_chunks)} chunks")
            except Exception as e:
                print(f"[red]❌ Error processing {file_path}: {e}[/red]")
                log.exception(f"Error processing {file_path}")
    
    # Generate embeddings and save the index
    if not chunks:
        print("[red]❌ No chunks generated, nothing to index[/red]")
        raise typer.Exit(1)
    
    total_chunks = len(chunks)
    print(f"\n🧠 Generating embeddings for {total_chunks} chunks...")
    try:
        vectors = get_embeddings(chunks)
        save_index_with_sources(vectors, chunks, sources, output_file)
        elapsed = time.time() - start_time
        print(f"✅ Index created with {total_chunks} chunks in {elapsed:.1f}s")
        print(f"📦 Saved to: {output_file}")
    except Exception as e:
        print(f"[red]❌ Error generating embeddings: {e}[/red]")
        log.exception("Error generating embeddings")
        raise typer.Exit(1)