from dataclasses import dataclass
from typing import Optional

@dataclass
class CompletionResult:
    index: int
    success: bool
    reasoning: str
    issues: Optional[str] = None
    improved_text: Optional[str] = None
    error_message: Optional[str] = None

    @classmethod
    def success(cls, index: int, reasoning: str, issues: str, improved_text: str):
        return cls(
            index=index,
            success=True,
            reasoning=reasoning,
            issues=issues,
            improved_text=improved_text
        )

    @classmethod
    def failure(cls, index: int, error_message: str):
        return cls(
            index=index,
            success=False,
            reasoning=error_message
        )
