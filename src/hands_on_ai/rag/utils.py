"""
Core RAG utilities for document loading, chunking, embedding, and retrieval.
"""

from pathlib import Path
import shutil
import importlib.resources
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI
from ..config import get_server_url, get_embedding_model, get_chunk_size, get_api_key


def load_text_file(path: Path) -> str:
    """
    Load text from various file formats.
    
    Args:
        path: Path to file
        
    Returns:
        str: Extracted text content
        
    Raises:
        ImportError: If required dependencies are missing
        ValueError: If file type is unsupported
    """
    ext = path.suffix.lower()

    if ext in [".txt", ".md"]:
        return path.read_text(encoding="utf-8")

    elif ext == ".docx":
        try:
            import docx
        except ImportError:
            raise ImportError("Please install `python-docx` to use .docx files. Try: pip install hands-on-ai[rag]")
        doc = docx.Document(path)
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    elif ext == ".pdf":
        try:
            import fitz  # PyMuPDF
        except ImportError:
            raise ImportError("Please install `pymupdf` to use .pdf files. Try: pip install hands-on-ai[rag]")
        with fitz.open(path) as doc:
            return "\n".join(page.get_text() for page in doc)

    else:
        raise ValueError(f"❌ Unsupported file type: {ext}. Supported: .txt, .md, .docx, .pdf")


def chunk_text(text, chunk_size=None):
    """
    Split text into chunks of approximately equal size.
    
    Args:
        text: Text to chunk
        chunk_size: Words per chunk (default from config)
        
    Returns:
        list: List of text chunks
    """
    if chunk_size is None:
        chunk_size = get_chunk_size()
        
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]


def get_embeddings(chunks, model=None):
    """
    Get embeddings for text chunks using the OpenAI-compatible embeddings API.

    This uses the same ``/v1`` endpoint and client as the rest of the package,
    so it works with any OpenAI-compatible provider (Ollama, OpenAI, etc.)
    rather than only Ollama's native ``/api/embeddings`` endpoint.

    Args:
        chunks: List of text chunks
        model: Embedding model to use (default from config)

    Returns:
        ndarray: Array of embedding vectors

    Raises:
        Exception: If embedding request fails
    """
    if model is None:
        model = get_embedding_model()

    server_url = get_server_url()
    # Add /v1 suffix for OpenAI-compatible endpoints
    if not server_url.endswith("/v1"):
        server_url = server_url.rstrip("/") + "/v1"

    client = OpenAI(
        base_url=server_url,
        api_key=get_api_key() or "hands-on-ai",
        timeout=30,
    )

    response = client.embeddings.create(model=model, input=list(chunks))
    # Sort by index so vector order matches the input chunk order.
    ordered = sorted(response.data, key=lambda item: item.index)
    return np.array([item.embedding for item in ordered])


def save_index_with_sources(vectors, chunks, sources, path):
    """
    Save RAG index with source tracking.
    
    Args:
        vectors: Embedding vectors
        chunks: Text chunks
        sources: Source information for each chunk
        path: Path to save index file
    """
    np.savez(path, vectors=vectors, chunks=np.array(chunks), sources=np.array(sources))


def load_index_with_sources(path):
    """
    Load RAG index with source tracking.
    
    Args:
        path: Path to index file
        
    Returns:
        tuple: (vectors, chunks, sources)
    """
    # allow_pickle=False prevents arbitrary code execution from a malicious
    # index file. chunks/sources are saved as plain string arrays, which load
    # fine without pickling.
    data = np.load(path, allow_pickle=False)
    return data["vectors"], data["chunks"], data["sources"]


def get_top_k(query, index_path, k=3, return_scores=False):
    """
    Retrieve top k similar chunks for a query.
    
    Args:
        query: Search query
        index_path: Path to index file
        k: Number of results to return
        return_scores: Whether to include similarity scores
        
    Returns:
        list: List of (chunk, source) tuples, optionally with scores
    """
    vectors, chunks, sources = load_index_with_sources(index_path)
    query_vector = get_embeddings([query])[0].reshape(1, -1)
    sims = cosine_similarity(query_vector, vectors)[0]
    top_indices = sims.argsort()[-k:][::-1]

    top_chunks = [chunks[i] for i in top_indices]
    top_sources = [sources[i] for i in top_indices]
    top_scores = [sims[i] for i in top_indices]

    if return_scores:
        return list(zip(top_chunks, top_sources)), top_scores
    return list(zip(top_chunks, top_sources))


def get_sample_docs_path():
    """
    Get the path to the sample document directory.
    
    Returns:
        Path: Path object to the sample documents directory
    """
    try:
        # For Python 3.9+
        with importlib.resources.path('hands_on_ai.rag.data', 'samples') as path:
            return path
    except Exception:
        # Fallback for older Python or direct file access
        module_path = Path(__file__).parent
        return module_path / 'data' / 'samples'


def list_sample_docs():
    """
    List all available sample documents.
    
    Returns:
        list: List of sample document filenames
    """
    sample_path = get_sample_docs_path()
    return [f.name for f in sample_path.iterdir() if f.is_file()]


def copy_sample_docs(destination=None):
    """
    Copy sample documents to a destination directory.
    
    Args:
        destination: Path to copy documents to (default: current directory)
        
    Returns:
        Path: Path to the destination directory
    """
    if destination is None:
        destination = Path.cwd() / 'sample_docs'
    else:
        destination = Path(destination)
        
    destination.mkdir(exist_ok=True, parents=True)
    sample_path = get_sample_docs_path()
    
    # Copy all files
    for file_path in sample_path.iterdir():
        if file_path.is_file():
            shutil.copy2(file_path, destination / file_path.name)
            
    return destination