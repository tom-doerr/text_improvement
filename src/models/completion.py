from dataclasses import dataclass
from typing import Optional

@dataclass
class CompletionResult:
    # Required fields first
    index: int
    success: bool
    reasoning: str
    issues: str
    improved_text: str
    # Optional fields with defaults last
    error_message: Optional[str] = None

    @classmethod
    def success(cls, index: int, reasoning: str, issues: str, improved_text: str):
        """Create a successful completion result"""
        return cls(
            index=index,
            success=True,
            reasoning=reasoning,
            issues=issues,
            improved_text=improved_text,
            error_message=None
        )

    @classmethod
    def failure(cls, index: int, error_message: str):
        """Create a failed completion result"""
        return cls(
            index=index,
            success=False,
            reasoning=error_message,  # Use error message as reasoning for display
            issues="",  # Empty string for failed completion
            improved_text="",  # Empty string for failed completion
            error_message=error_message
        )
