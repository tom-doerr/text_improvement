from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class CompletionResult:
    """
    Represents the result of a completion generation attempt.
    All fields are required to ensure proper initialization order.
    The factory methods handle creating appropriate values for success/failure cases.
    """
    # Required fields that are always meaningful
    index: int
    success: bool
    
    # Content fields - will contain real content or error message
    reasoning: str
    
    # Optional fields - empty strings in failure case
    issues: str = ""
    improved_text: str = ""
    error_message: str = ""

    @classmethod
    def success(cls, index: int, reasoning: str, issues: str, improved_text: str) -> 'CompletionResult':
        """Create a successful completion result"""
        return cls(
            index=index,
            success=True,
            reasoning=reasoning,
            issues=issues,
            improved_text=improved_text
        )

    @classmethod
    def failure(cls, index: int, error_message: str) -> 'CompletionResult':
        """Create a failed completion result"""
        return cls(
            index=index,
            success=False,
            reasoning=error_message,
            error_message=error_message
        )
