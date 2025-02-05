from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class CompletionResult:
    """
    Represents the result of a completion generation attempt.
    All fields are required to ensure proper initialization order.
    The factory methods handle creating appropriate values for success/failure cases.
    """
    index: int
    success: bool
    reasoning: str
    issues: str
    improved_text: str
    error_message: str

    @classmethod
    def success(cls, index: int, reasoning: str, issues: str, improved_text: str) -> 'CompletionResult':
        """Create a successful completion result"""
        return cls(
            index=index,
            success=True,
            reasoning=reasoning,
            issues=issues,
            improved_text=improved_text,
            error_message=""  # No error for successful completion
        )

    @classmethod
    def failure(cls, index: int, error_message: str) -> 'CompletionResult':
        """Create a failed completion result"""
        return cls(
            index=index,
            success=False,
            reasoning=error_message,  # Use error message as reasoning for display
            issues="",               # Empty string for failed completion
            improved_text="",        # Empty string for failed completion
            error_message=error_message
        )
