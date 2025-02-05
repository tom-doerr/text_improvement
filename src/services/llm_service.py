import dspy
from typing import Tuple, List
from ..models.example import Example

class LLMService:
    def __init__(self):
        # Configure LLM with default settings
        dspy.settings.configure(
            lm=dspy.LM(
                'openrouter/anthropic/claude-3.5-sonnet',
                temperature=2.0,
                cache=False,
                max_tokens=300
            )
        )

    def generate_completion(
        self,
        examples: List[Example],
        instruction: str,
        input_text: str
    ) -> Tuple[str, str, str]:
        """
        Generate a completion using the configured LLM.
        Returns tuple of (reasoning, issues, improved_text)
        """
        if not instruction:
            instruction = "Improve the text by fixing any issues with grammar, clarity, and style."
            
        if not input_text.strip():
            raise ValueError("Input text cannot be empty")
            
        from simpledspy import pipe
        return pipe(
            [ex.to_dict() for ex in examples],
            instruction,
            input_text
        )
