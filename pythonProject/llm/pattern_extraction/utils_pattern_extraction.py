import os
import dspy
import pickle
from pathlib import Path
from typing import Any, Optional

from ..connectors.dspy import DSPy
from ..connectors.dspy_LMs.claude_chat import ClaudeChat
from .pattern_description_signature import PatternDescriptionSignature
from .pattern_extraction_signature import PatternExtractionSignature

claude = dspy.Claude("claude-3-5-sonnet-20240620", api_key=os.environ.get('ANTHROPIC_API_KEY'))
claude_chat1 = ClaudeChat("claude-3-5-sonnet-20240620", api_key=os.environ.get('ANTHROPIC_API_KEY'))
claude_chat2 = ClaudeChat("claude-3-5-sonnet-20240620", api_key=os.environ.get('ANTHROPIC_API_KEY'))

dspy_pattern_descriptor = DSPy(strategy_method='one_shot', system_info='', model=claude, chat_model=claude_chat1, io_signature=PatternDescriptionSignature)
dspy_pattern_extractor = DSPy(strategy_method='one_shot', system_info='', model=claude, chat_model=claude_chat2, io_signature=PatternExtractionSignature)


def log_interaction(log_file: str, prompt: str, response: str):
    """Log the interaction between the system and the LLM."""
    with open(log_file, 'a') as f:
        f.write(f"Prompt: {prompt}\n\n")
        f.write(f"Response: {response}\n\n")
        f.write("-" * 80 + "\n\n")

def load_cached_data(filename: Path) -> Optional[Any]:
    """Load cached data from a file."""
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except (FileNotFoundError, pickle.UnpicklingError):
        return None

def save_cached_data(filename: Path, data: Any):
    """Save data to a cache file."""
    with open(filename, "wb") as file:
        pickle.dump(data, file)

    