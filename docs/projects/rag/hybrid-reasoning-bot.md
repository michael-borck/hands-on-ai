# Hybrid Reasoning Bot

**Difficulty**: Intermediate  
**Time**: 60 minutes  
**Learning Focus**: RAG, similarity thresholds, fallback logic  
**Module**: RAG

## Overview
Create a bot that intelligently chooses between using your indexed documents (RAG) or the model's general knowledge based on similarity scores. The bot tags responses with source indicators to clearly show where information is coming from.

## Instructions

1. **Set up the project:**
   - Create a new Python script file
   - Import the necessary libraries from hands-on-ai - Define emoji constants for tagging sources (🧠 = from notes, 🌐 = fallback)

2. **Build an index first:**
   - Run `rag index path/to/your/docs/` to create `~/.hands-on-ai/index.npz`

3. **Create the retrieval function:**
   - Use `get_top_k(query, index_path, k, return_scores=True)` to retrieve the
     top-K `(chunk, source)` pairs together with their similarity scores

4. **Build answer generation functions:**
   - Create a RAG-based answer function that uses retrieved chunks as context
   - Create a fallback function that uses only the LLM's general knowledge

5. **Implement the decision logic:**
   - Use similarity threshold (e.g., 0.7) to decide between RAG or fallback
   - Tag responses appropriately with source indicators

6. **Add command-line argument handling:**
   - Query input
   - Index file path
   - Similarity threshold
   - Top-K value
   - Optional flags for comparing answers and showing scores

7. **Test your implementation:**
   - Try queries with obvious matches in your index
   - Try queries with no relevant information in your index
   - Experiment with different threshold values


```python
#!/usr/bin/env python3
"""
Hybrid Reasoning Bot
-------------------
A bot that chooses between RAG or general LLM answers based on similarity score.
It uses your indexed documents when it finds relevant information,
and falls back to general knowledge when necessary.
"""

import argparse
from hands_on_ai.chat import get_response
from hands_on_ai.rag.utils import get_top_k

# Emoji constants
RAG_TAG = "🧠"  # Knowledge from your notes/documents
LLM_TAG = "🌐"  # Knowledge from the model's training

def get_chunks_with_scores(query, index_path, top_k=3):
    """Retrieve the most relevant (chunk, source) pairs and their similarity scores."""
    # get_top_k embeds the query, loads the index, and runs the search.
    results, scores = get_top_k(query, index_path, k=top_k, return_scores=True)
    return results, scores

def generate_rag_answer(query, chunks):
    """Generate an answer using RAG with the provided chunks as context"""
    context = "\n\n---\n\n".join(chunks)

    prompt = f"""Based on the following information, please answer the question.
If the information doesn't fully address the question, use only what's relevant.

Context:
{context}

Question: {query}

Answer:"""
    return get_response(prompt)

def generate_llm_answer(query):
    """Generate an answer using only the LLM's general knowledge"""
    prompt = f"""Please answer this question based on your general knowledge:

Question: {query}

Answer:"""
    return get_response(prompt)

def main():
    parser = argparse.ArgumentParser(description="Hybrid reasoning bot using RAG and general knowledge")
    parser.add_argument("query", help="The question to ask")
    parser.add_argument("--index", "-i", default="index.npz", help="Path to the .npz index file")
    parser.add_argument("--threshold", "-t", type=float, default=0.7, 
                        help="Similarity score threshold for using RAG (0.0-1.0)")
    parser.add_argument("--top-k", "-k", type=int, default=3, 
                        help="Number of chunks to use when generating RAG answers")
    parser.add_argument("--no-fallback", "-n", action="store_true", 
                        help="Disable fallback to general knowledge even with low scores")
    parser.add_argument("--compare", "-c", action="store_true", 
                        help="Show both RAG and general knowledge answers for comparison")
    parser.add_argument("--show-scores", "-s", action="store_true", 
                        help="Show similarity scores for retrieved chunks")
    args = parser.parse_args()

    # Retrieve relevant (chunk, source) pairs and their scores
    print(f"Searching index: {args.index}...")
    results, scores = get_chunks_with_scores(args.query, args.index, top_k=args.top_k)
    top_chunks = [chunk for chunk, _ in results]

    # Determine if we should use RAG based on the highest similarity score
    best_score = max(scores) if scores else 0
    use_rag = best_score >= args.threshold

    # Show scores if requested
    if args.show_scores:
        print("\n=== Similarity Scores ===")
        for i, ((chunk, source), score) in enumerate(zip(results, scores)):
            print(f"[{i+1}] Score: {score:.4f}  Source: {source}")
            print(f"Preview: {chunk[:100]}...\n")
        print(f"Best score: {best_score:.4f} (Threshold: {args.threshold})")
        print(f"Decision: {'Using RAG' if use_rag else 'Using general knowledge'}\n")

    # Generate answers
    if args.compare:
        # Generate both answers for comparison
        print("\n=== Generating both answers for comparison ===")

        print(f"\n{RAG_TAG} Generating answer from your documents...")
        rag_answer = generate_rag_answer(args.query, top_chunks)

        print(f"\n{LLM_TAG} Generating answer from general knowledge...")
        llm_answer = generate_llm_answer(args.query)

        # Display both answers
        print(f"\n=== {RAG_TAG} Answer from your documents ===")
        print(rag_answer)

        print(f"\n=== {LLM_TAG} Answer from general knowledge ===")
        print(llm_answer)

    else:
        # Generate only one answer based on the threshold
        if use_rag or args.no_fallback:
            tag = RAG_TAG
            print(f"\n{tag} Generating answer from your documents...")
            answer = generate_rag_answer(args.query, top_chunks)
        else:
            tag = LLM_TAG
            print(f"\n{tag} No sufficiently relevant information found in your documents.")
            print(f"{tag} Falling back to general knowledge...")
            answer = generate_llm_answer(args.query)

        # Display the answer
        print(f"\n=== {tag} Answer ===")
        print(answer)

    # Show sources if using RAG
    if use_rag or args.no_fallback or args.compare:
        print("\n=== Sources ===")
        for source in {source for _, source in results}:
            print(f"- {source}")

if __name__ == "__main__":
    main()
```
## Extension Ideas

1. **Enhanced Source Attribution**: Display specific document names and page numbers for RAG answers
2. **Confidence Visualization**: Create a visual representation of similarity scores 
3. **Hybrid Answers**: Combine information from both sources when appropriate
4. **Interactive Mode**: Create a chat-like interface that remembers context
5. **Custom Personalities**: Allow different personality settings for different query types
6. **Performance Metrics**: Track and display response times for both methods
7. **Web Interface**: Create a simple web UI for the hybrid bot
