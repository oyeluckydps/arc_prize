from ..connectors.dspy import DSPy
from ..utils import claude, claude_chat1, claude_chat2

from .signatures.pattern_description_signature import DetailedPatternDescriptionSignature
from .short_pattern_description_signature import ShortPatternDescriptionSignature
from .signatures.most_relevant_pattern_description_signature import MostRelevantPatternDescriptionSignature
from .signatures.pattern_extraction_signature import PatternExtractionSignature


dspy_detailed_pattern_descriptor = DSPy(strategy_method='one_shot', system_info='', model=claude, chat_model=claude_chat1, io_signature=DetailedPatternDescriptionSignature)
dspy_short_pattern_descriptor = DSPy(strategy_method='one_shot', system_info='', model=claude, chat_model=claude_chat1, io_signature=ShortPatternDescriptionSignature)
dspy_most_relevant_pattern_descriptor = DSPy(strategy_method='one_shot', system_info='', model=claude, chat_model=claude_chat1, io_signature=MostRelevantPatternDescriptionSignature)
dspy_pattern_extractor = DSPy(strategy_method='one_shot', system_info='', model=claude, chat_model=claude_chat2, io_signature=PatternExtractionSignature)
