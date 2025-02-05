from dataclasses import dataclass
from typing import Optional

@dataclass
class CompletionResult:
    """
    Represents the result of a completion generation attempt.
    All fields are required to avoid dataclass field ordering issues.
    """
    index: int
    success: bool
    error_message: str  # Empty string if success=True
    reasoning: str      # Contains error message if success=False
    issues: str        # Empty string if success=False
    improved_text: str  # Empty string if success=False

    @classmethod
    def success(cls, index: int, reasoning: str, issues: str, improved_text: str):
        """Create a successful completion result"""
        return cls(
            index=index,
            success=True,
            error_message="",  # No error for successful completion
            reasoning=reasoning,
            issues=issues,
            improved_text=improved_text
        )

    @classmethod
    def failure(cls, index: int, error_message: str):
        """Create a failed completion result"""
        return cls(
            index=index,
            success=False,
            error_message=error_message,
            reasoning=error_message,  # Use error message as reasoning for display
            issues="",               # Empty string for failed completion
            improved_text=""         # Empty string for failed completion
        )
