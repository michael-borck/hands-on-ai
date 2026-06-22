"""
Text analysis tools for processing and analyzing text content.

This agent provides tools for analyzing text, including word counting,
readability scoring, and text summarization.
"""

import re
import math
from ..core import register_tool

def word_count(text: str) -> str:
    """
    Count words, characters, sentences, and paragraphs in a text.
    
    Args:
        text: The text to analyze
        
    Returns:
        str: Statistics about the text
    """
    if not text.strip():
        return "Empty text provided."
    
    # Count characters
    char_count = len(text)
    char_count_no_spaces = len(text.replace(" ", ""))
    
    # Count words
    words = re.findall(r'\b\w+\b', text.lower())
    word_count = len(words)
    
    # Count unique words
    unique_words = len(set(words))
    
    # Count sentences (roughly)
    sentences = re.split(r'[.!?]+', text)
    sentence_count = len([s for s in sentences if s.strip()])
    
    # Count paragraphs
    paragraphs = text.split('\n\n')
    paragraph_count = len([p for p in paragraphs if p.strip()])
    
    # Average word length
    avg_word_length = sum(len(word) for word in words) / max(1, word_count)
    
    # Format the results
    results = [
        f"Word count: {word_count}",
        f"Character count: {char_count}",
        f"Character count (without spaces): {char_count_no_spaces}",
        f"Sentence count: {sentence_count}",
        f"Paragraph count: {paragraph_count}",
        f"Unique words: {unique_words}",
        f"Average word length: {avg_word_length:.1f} characters"
    ]
    
    return "\n".join(results)


def readability_score(text: str) -> str:
    """
    Calculate readability metrics for a given text.
    
    Args:
        text: The text to analyze
        
    Returns:
        str: Readability scores and grade levels
    """
    if not text.strip():
        return "Empty text provided."
    
    # Count words
    words = re.findall(r'\b\w+\b', text.lower())
    word_count = len(words)
    
    if word_count == 0:
        return "No words found in the text."
    
    # Count sentences (roughly)
    sentences = re.split(r'[.!?]+', text)
    sentence_count = len([s for s in sentences if s.strip()])
    
    if sentence_count == 0:
        return "No sentences found in the text."
    
    # Count syllables (approximate method)
    def count_syllables(word):
        word = word.lower()
        if len(word) <= 3:
            return 1
        
        # Remove es, ed endings
        word = re.sub(r'e$|es$|ed$', '', word)
        
        # Count vowel groups
        count = len(re.findall(r'[aeiouy]+', word))
        return max(1, count)
    
    syllable_count = sum(count_syllables(word) for word in words)
    
    # Calculate metrics
    words_per_sentence = word_count / sentence_count
    syllables_per_word = syllable_count / word_count
    
    # Flesch Reading Ease
    flesch_ease = 206.835 - (1.015 * words_per_sentence) - (84.6 * syllables_per_word)
    flesch_ease = max(0, min(100, flesch_ease))  # Clamp between 0 and 100
    
    # Flesch-Kincaid Grade Level
    fk_grade = 0.39 * words_per_sentence + 11.8 * syllables_per_word - 15.59
    fk_grade = max(0, fk_grade)  # Ensure it's not negative
    
    # SMOG Index (simplified)
    smog = 1.043 * math.sqrt(syllable_count * (30 / sentence_count)) + 3.1291
    
    # Interpret Flesch Reading Ease
    if flesch_ease >= 90:
        flesch_interpretation = "Very Easy (5th grade)"
    elif flesch_ease >= 80:
        flesch_interpretation = "Easy (6th grade)"
    elif flesch_ease >= 70:
        flesch_interpretation = "Fairly Easy (7th grade)"
    elif flesch_ease >= 60:
        flesch_interpretation = "Standard (8-9th grade)"
    elif flesch_ease >= 50:
        flesch_interpretation = "Fairly Difficult (10-12th grade)"
    elif flesch_ease >= 30:
        flesch_interpretation = "Difficult (College level)"
    else:
        flesch_interpretation = "Very Difficult (College graduate level)"
    
    # Format the results
    results = [
        f"Flesch Reading Ease: {flesch_ease:.1f} - {flesch_interpretation}",
        f"Flesch-Kincaid Grade Level: {fk_grade:.1f}",
        f"SMOG Index: {smog:.1f}",
        "",
        "Statistics:",
        f"- Sentences: {sentence_count}",
        f"- Words: {word_count}",
        f"- Syllables: {syllable_count}",
        f"- Words per sentence: {words_per_sentence:.1f}",
        f"- Syllables per word: {syllables_per_word:.1f}"
    ]
    
    return "\n".join(results)


def summarize(text: str, ratio: str = "0.3") -> str:
    """
    Create a simple extractive summary of the given text.
    
    Args:
        text: The text to summarize
        ratio: The proportion of sentences to include in the summary (0.1 to 0.5)
        
    Returns:
        str: A summary of the text
    """
    if not text.strip():
        return "Empty text provided."
    
    # Convert ratio to float and validate
    try:
        ratio_float = float(ratio)
        if ratio_float < 0.1:
            ratio_float = 0.1
        elif ratio_float > 0.5:
            ratio_float = 0.5
    except ValueError:
        return f"Invalid ratio: {ratio}. Please provide a number between 0.1 and 0.5."
    
    # Split text into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    if len(sentences) <= 3:
        return "Text is too short to summarize."
    
    # Score sentences based on word frequency
    # 1. Calculate word frequency
    words = re.findall(r'\b\w+\b', text.lower())
    word_freq: dict[str, int] = {}
    for word in words:
        if len(word) > 3:  # Skip short words
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # 2. Score each sentence based on word frequency
    sentence_scores = []
    for i, sentence in enumerate(sentences):
        if not sentence.strip():
            continue
        
        # Calculate score based on word frequency
        words_in_sentence = re.findall(r'\b\w+\b', sentence.lower())
        score = sum(word_freq.get(word, 0) for word in words_in_sentence)
        
        # Favor sentences near the beginning and end
        position_factor = 1.0
        if i < len(sentences) * 0.2:  # First 20% of sentences
            position_factor = 1.2
        elif i > len(sentences) * 0.8:  # Last 20% of sentences
            position_factor = 1.1
        
        sentence_scores.append((i, sentence, score * position_factor))
    
    # 3. Select top sentences based on ratio
    num_sentences = max(1, int(len(sentences) * ratio_float))
    top_sentences = sorted(sentence_scores, key=lambda x: x[2], reverse=True)[:num_sentences]
    
    # 4. Sort sentences by original position
    summary_sentences = sorted(top_sentences, key=lambda x: x[0])
    
    # 5. Join the selected sentences
    summary = " ".join(sentence for _, sentence, _ in summary_sentences)
    
    return summary


def register_text_tools():
    """Register all text analysis tools with the agent."""
    register_tool(
        "word_count",
        "Count words, characters, sentences, and paragraphs in a text",
        word_count
    )
    
    register_tool(
        "readability",
        "Calculate readability scores (Flesch Reading Ease, grade level) for text",
        readability_score
    )
    
    register_tool(
        "summarize",
        "Create a summary of text (ratio parameter controls length, 0.1-0.5)",
        summarize
    )