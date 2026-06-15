# Build Your Own QandA CLI

**Difficulty**: Intermediate  
**Time**: 45 minutes  
**Learning Focus**: RAG, Embeddings, Vector Search, CLI Development  
**Module**: RAG

## Overview
Create a command-line interface (CLI) tool that implements Retrieval-Augmented Generation (RAG) to answer questions based on your own knowledge index. This project will teach you how to programmatically load vector embeddings, perform similarity searches, and generate contextually relevant responses.

## Instructions

1. **Setup Your Environment**
   - Ensure you have Python 3.10+ installed
   - Install the library: `pip install hands-on-ai`
   - Build an index from your documents first:
     ```bash
     rag index path/to/your/docs/
     ```
     This writes an index to `~/.hands-on-ai/index.npz` by default.

2. **Understanding the Components**
   - Learn how RAG combines retrieval and generation
   - Understand embeddings and cosine similarity for semantic search
   - Explore the retrieval helper in `hands_on_ai.rag.utils`:
     `get_top_k(query, index_path, k=3, return_scores=False)`. It embeds the
     query, loads the index, runs the similarity search, and returns a list of
     `(chunk, source)` tuples, optionally with scores.

3. **Build Your CLI Script**
   - Create a Python script with the following functions:
     - `query_index()`: Retrieve the most similar chunks for a query
     - `generate_answer()`: Create a response using retrieved context
     - `main()`: Handle CLI arguments and orchestrate the workflow

4. **Sample Implementation**
   ```python
   #!/usr/bin/env python3
   """
   Simple Q&A CLI using RAG (Retrieval-Augmented Generation)
   This script retrieves relevant chunks from an index and generates answers.
   """

   import argparse
   from hands_on_ai.chat import get_response
   from hands_on_ai.rag.utils import get_top_k

   def query_index(query, index_path, top_k=3, show_scores=False):
       """Retrieve the top K most relevant chunks for a query."""
       print(f"Processing query: '{query}'")

       # get_top_k embeds the query, loads the index, and runs the search.
       # It returns a list of (chunk, source) tuples.
       if show_scores:
           results, scores = get_top_k(query, index_path, k=top_k, return_scores=True)
       else:
           results, scores = get_top_k(query, index_path, k=top_k), None

       context = "\n\n---\n\n".join(chunk for chunk, _ in results)

       if show_scores:
           print("\n=== Top Chunks ===")
           for i, ((chunk, source), score) in enumerate(zip(results, scores)):
               print(f"[{i+1}] Score: {score:.4f}  Source: {source}")
               print(f"Preview: {chunk[:100]}...\n")

       return context, results

   def generate_answer(query, context):
       """Generate a response using the retrieved context."""
       prompt = f"""Based on the following context, please answer the question. If the context doesn't contain relevant information to answer the question fully, say what you can based on the context and indicate what information is missing.

   Context:
   {context}

   Question: {query}

   Answer:"""
       return get_response(prompt)

   def main():
       parser = argparse.ArgumentParser(description="Query a RAG index and get answers.")
       parser.add_argument("query", help="The question to ask")
       parser.add_argument("--index", "-i", default="index.npz", help="Path to the .npz index file")
       parser.add_argument("--top-k", "-k", type=int, default=3, help="Number of chunks to retrieve")
       parser.add_argument("--show-scores", "-s", action="store_true", help="Show similarity scores and chunk previews")
       parser.add_argument("--show-context", "-c", action="store_true", help="Show full context used for generation")
       args = parser.parse_args()

       context, results = query_index(
           args.query, args.index, top_k=args.top_k, show_scores=args.show_scores
       )

       if args.show_context:
           print("\n=== Full Context ===")
           print(context)
           print()

       print("\n=== Answer ===")
       print(generate_answer(args.query, context))

       # Show which sources the answer drew from
       print("\n=== Sources ===")
       for source in {source for _, source in results}:
           print(f"- {source}")

   if __name__ == "__main__":
       main()
   ```

5. **Test Your Implementation**
   - Point `--index` at the index you built (default `~/.hands-on-ai/index.npz`)
   - Run your script with various queries
   - Experiment with different `top_k` values to see how it affects answers

## Extension Ideas

1. **Add More CLI Options**
   - Implement a `--temperature` flag to control response randomness
   - Add a `--model` option to select different LLMs for response generation
   - Create a `--format` flag to return responses as JSON or markdown

2. **Enhance Result Quality**
   - Implement re-ranking of retrieved chunks using cross-encoders
   - Add chunk summarization before combining context
   - Create a custom scoring mechanism that considers both relevance and recency

3. **Build a Web Interface**
   - Create a simple Flask or Streamlit app that uses your RAG engine
   - Add visualization of similarity scores or chunk relationships
   - Implement user feedback collection to improve retrieval quality

4. **Performance Optimizations**
   - Add caching for query embeddings and responses
   - Implement batched query processing for multiple questions
   - Explore approximate nearest neighbor algorithms for faster retrieval on large indices