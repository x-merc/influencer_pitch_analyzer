from datetime import datetime
import sys
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

sys.path.append("./")


class ScriptSubmission(BaseModel):
    content: str
    creator_name: str
    submission_date: datetime = Field(default_factory=datetime.now)
    brief_type: Optional[str] = None
