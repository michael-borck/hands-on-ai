# My First RAG Bot

**Difficulty**: Intermediate  
**Time**: 45 minutes  
**Learning Focus**: Document indexing, vector retrieval, context-based generation  
**Module**: RAG

## Overview
Learn how to use the `rag` CLI to index documents and create a simple Retrieval-Augmented Generation (RAG) system that can answer questions based on your own notes or documents.

## Instructions

### Step 1: Set up your environment
1. Install the `rag` CLI tool:
   ```bash
   pip install hands-on-ai
   ```
2. Ensure you have access to the `testdata/demo_notes/` directory or prepare your own documents

### Step 2: Index your documents
1. Browse through the available demo documents:
   ```bash
   ls hands_on_ai/testdata/demo_notes/
   ```
2. Create an index of all documents in the demo notes directory:
   ```bash
   rag index hands_on_ai/testdata/demo_notes/
   ```
3. Observe the output showing how many files were found and processed. By default the index is saved to `~/.hands-on-ai/index.npz` (so `rag ask` finds it automatically).

### Step 3: Ask questions using your RAG system
1. Ask a basic question about the content:
   ```bash
   rag ask "What does TCP do?" --context
   ```
2. Try different questions to explore the content:
   ```bash
   rag ask "How does HTTP work?" --context
   rag ask "What is the difference between TCP and UDP?" --scores
   ```
3. Experiment with different flags:
   - `--context` (`-c`): See what information was used to answer
   - `--scores` (`-s`): View relevance ranking of different text chunks
   - `--k 5`: Retrieve 5 most relevant chunks instead of default 3

### Step 4: Understand how RAG works
1. Review how the system processes your request:
   - Documents are broken into smaller chunks
   - Vector embeddings are created for each chunk
   - When you ask a question, it finds chunks with similar embeddings
   - Retrieved chunks are used as context for generating an answer

## Extension Ideas

1. **Create your own knowledge base**:
   - Create markdown files with your class notes or research
   - Index them and ask questions to test your understanding

2. **Experiment with different file types**:
   - Add PDF files to your document collection
   - Re-index to include the new files
   - Compare how well the system handles different formats

3. **Build a specialized RAG system**:
   - Create a collection of documents on a specific topic
   - Develop a set of test questions to evaluate retrieval quality
   - Fine-tune your prompts to get better answers

4. **Analyze retrieval performance**:
   - Use the `--scores` flag to see how different chunks are ranked
   - Experiment with question phrasing to improve retrieval accuracy
   - Try adjusting the number of chunks retrieved with `--top-k`