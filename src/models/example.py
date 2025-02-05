from dataclasses import dataclass

@dataclass
class Example:
    input_text: str
    reasoning: str
    issues: str
    improved_text: str

    def to_dict(self) -> dict:
        return {
            'input_text': self.input_text,
            'reasoning': self.reasoning,
            'issues': self.issues,
            'improved_text': self.improved_text
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Example':
        return cls(
            input_text=data['input_text'],
            reasoning=data['reasoning'],
            issues=data['issues'],
            improved_text=data['improved_text']
        )
