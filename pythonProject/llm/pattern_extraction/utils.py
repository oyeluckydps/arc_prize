import os
import dspy
from ..connectors.dspy import DSPy
from ..connectors.dspy_LMs.claude_chat import ClaudeChat
from pattern_description_signature import PatternDescriptionSignature
from pattern_extraction_signature import PatternExtractionSignature

claude = dspy.Claude("claude-3-5-sonnet-20240620", api_key=os.environ.get('ANTHROPIC_API_KEY'))
claude_chat1 = ClaudeChat("claude-3-5-sonnet-20240620", api_key=os.environ.get('ANTHROPIC_API_KEY'))
claude_chat2 = ClaudeChat("claude-3-5-sonnet-20240620", api_key=os.environ.get('ANTHROPIC_API_KEY'))

dspy_pattern_descriptor = DSPy(strategy_method='chat', system_info='', model=claude, chat_model=claude_chat1, io_signature=PatternDescriptionSignature)
dspy_pattern_extractor = DSPy(strategy_method='chat', system_info='', model=claude, chat_model=claude_chat2, io_signature=PatternExtractionSignature)