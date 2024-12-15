import sys
from typing import List, Dict, Optional
from pydantic import BaseModel

sys.path.append("./")


class AnalysisResult(BaseModel):
    criteria: str
    passed: bool
    feedback: str
    suggestions: Optional[List[str]] = None

    def to_dict(self):
        # Convert the object to a dictionary format
        return {
            "criteria": self.criteria,
            "passed": self.passed,
            "feedback": self.feedback,
            "suggestions": self.suggestions,
        }
