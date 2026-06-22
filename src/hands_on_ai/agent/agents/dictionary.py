"""
Dictionary agent for language assistance.

This agent provides tools for looking up word definitions, synonyms, antonyms, 
and examples. It uses a built-in dictionary for basic functionality without 
requiring external API calls.
"""

from ..core import register_tool

# Simple built-in dictionary with common words
# In a real implementation, this would be more extensive or use an API
MINI_DICTIONARY = {
    "hello": {
        "definition": "Used as a greeting or to begin a conversation.",
        "synonyms": ["hi", "greetings", "hey", "howdy"],
        "antonyms": ["goodbye", "bye"],
        "examples": ["Hello, how are you?", "She said hello to everyone she met."]
    },
    "happy": {
        "definition": "Feeling or showing pleasure or contentment.",
        "synonyms": ["joyful", "cheerful", "delighted", "pleased", "content"],
        "antonyms": ["sad", "unhappy", "miserable", "depressed"],
        "examples": ["I'm happy to see you.", "They were a happy family."]
    },
    "sad": {
        "definition": "Feeling or showing sorrow; unhappy.",
        "synonyms": ["unhappy", "sorrowful", "dejected", "depressed", "downcast"],
        "antonyms": ["happy", "joyful", "cheerful"],
        "examples": ["I feel sad about leaving.", "It was a sad occasion."]
    },
    "big": {
        "definition": "Of considerable size, extent, or intensity.",
        "synonyms": ["large", "huge", "enormous", "gigantic", "substantial"],
        "antonyms": ["small", "tiny", "little", "miniature"],
        "examples": ["A big house", "That's a big problem."]
    },
    "small": {
        "definition": "Of a size that is less than normal or usual.",
        "synonyms": ["little", "tiny", "miniature", "compact", "diminutive"],
        "antonyms": ["big", "large", "huge", "enormous"],
        "examples": ["A small house", "Only a small number of people attended."]
    },
    "run": {
        "definition": "Move at a speed faster than a walk, never having both feet on the ground at the same time.",
        "synonyms": ["sprint", "jog", "dash", "race", "gallop"],
        "antonyms": ["walk", "stroll", "amble"],
        "examples": ["She runs every morning.", "He ran to catch the bus."]
    },
    "walk": {
        "definition": "Move at a regular pace by lifting and setting down each foot in turn, never having both feet off the ground at once.",
        "synonyms": ["stroll", "amble", "wander", "trudge", "stride"],
        "antonyms": ["run", "sprint", "dash"],
        "examples": ["We walked to the store.", "He walks his dog every evening."]
    },
    "learn": {
        "definition": "Gain or acquire knowledge of or skill in (something) by study, experience, or being taught.",
        "synonyms": ["study", "discover", "grasp", "master", "comprehend"],
        "antonyms": ["forget", "ignore", "misunderstand"],
        "examples": ["She learned French.", "Children learn quickly."]
    },
    "teach": {
        "definition": "Impart knowledge to or instruct (someone) as to how to do something.",
        "synonyms": ["instruct", "educate", "train", "coach", "tutor"],
        "antonyms": ["learn", "study"],
        "examples": ["She teaches math.", "He taught me how to swim."]
    },
    "good": {
        "definition": "To be desired or approved of; having the required qualities; of a high standard.",
        "synonyms": ["excellent", "fine", "wonderful", "superb", "quality"],
        "antonyms": ["bad", "poor", "inferior", "substandard"],
        "examples": ["Good work!", "The food was very good."]
    },
    "bad": {
        "definition": "Of poor quality or a low standard; not satisfactory or pleasing.",
        "synonyms": ["poor", "inferior", "substandard", "deficient", "inadequate"],
        "antonyms": ["good", "excellent", "superior", "quality"],
        "examples": ["Bad weather", "I had a bad day."]
    }
}


def define(word: str) -> str:
    """
    Look up the definition of a word.
    
    Args:
        word: The word to define
        
    Returns:
        str: The definition or an error message
    """
    word = word.lower().strip()
    
    if word in MINI_DICTIONARY:
        return str(MINI_DICTIONARY[word]["definition"])
    else:
        # Using built-in dictionary for words not in our mini dictionary
        # In a full implementation, this would use an API or larger database
        return f"Sorry, I don't have a definition for '{word}' in my dictionary."


def get_synonyms(word: str) -> str:
    """
    Find synonyms for a word.
    
    Args:
        word: The word to find synonyms for
        
    Returns:
        str: A list of synonyms or an error message
    """
    word = word.lower().strip()
    
    if word in MINI_DICTIONARY and "synonyms" in MINI_DICTIONARY[word]:
        synonyms = MINI_DICTIONARY[word]["synonyms"]
        if synonyms:
            return f"Synonyms for '{word}': {', '.join(synonyms)}"
        else:
            return f"No synonyms found for '{word}'."
    else:
        return f"Sorry, I don't have synonyms for '{word}' in my dictionary."


def get_antonyms(word: str) -> str:
    """
    Find antonyms for a word.
    
    Args:
        word: The word to find antonyms for
        
    Returns:
        str: A list of antonyms or an error message
    """
    word = word.lower().strip()
    
    if word in MINI_DICTIONARY and "antonyms" in MINI_DICTIONARY[word]:
        antonyms = MINI_DICTIONARY[word]["antonyms"]
        if antonyms:
            return f"Antonyms for '{word}': {', '.join(antonyms)}"
        else:
            return f"No antonyms found for '{word}'."
    else:
        return f"Sorry, I don't have antonyms for '{word}' in my dictionary."


def get_examples(word: str) -> str:
    """
    Find example sentences using a word.
    
    Args:
        word: The word to find examples for
        
    Returns:
        str: Example sentences or an error message
    """
    word = word.lower().strip()
    
    if word in MINI_DICTIONARY and "examples" in MINI_DICTIONARY[word]:
        examples = MINI_DICTIONARY[word]["examples"]
        if examples:
            examples_text = "\n".join([f"- {example}" for example in examples])
            return f"Examples for '{word}':\n{examples_text}"
        else:
            return f"No examples found for '{word}'."
    else:
        return f"Sorry, I don't have examples for '{word}' in my dictionary."


def register_dictionary_agent():
    """Register all dictionary tools with the agent."""
    register_tool(
        "define",
        "Look up the definition of a word",
        define
    )
    
    register_tool(
        "synonyms",
        "Find synonyms (words with similar meaning) for a word",
        get_synonyms
    )
    
    register_tool(
        "antonyms",
        "Find antonyms (words with opposite meaning) for a word",
        get_antonyms
    )
    
    register_tool(
        "examples",
        "Find example sentences using a word",
        get_examples
    )