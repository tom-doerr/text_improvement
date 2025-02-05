from dataclasses import dataclass
from typing import Optional

@dataclass
class CompletionResult:
    index: int
    success: bool
    error_message: Optional[str]
    reasoning: str
    issues: str
    improved_text: str

    @classmethod
    def success(cls, index: int, reasoning: str, issues: str, improved_text: str):
        return cls(
            index=index,
            success=True,
            error_message=None,
            reasoning=reasoning,
            issues=issues,
            improved_text=improved_text
        )

    @classmethod
    def failure(cls, index: int, error_message: str):
        return cls(
            index=index,
            success=False,
            error_message=error_message,
            reasoning=error_message,
            issues="",
            improved_text=""
        )
