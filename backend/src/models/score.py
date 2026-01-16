"""
Score model - Represents a grading outcome
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid


class Score(BaseModel):
    """Data model for scores"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    result_id: str = Field(...)
    grader_id: str = Field(...)
    passed: bool = Field(...)
    score: Optional[float] = Field(None, ge=0.0, le=1.0)
    details: Optional[dict] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "score-1",
                "result_id": "result-1",
                "grader_id": "string-match",
                "passed": True,
                "score": 1.0,
                "details": {
                    "expected": "Paris",
                    "actual": "Paris",
                    "match": "exact"
                },
                "created_at": "2026-01-15T10:35:02Z"
            }
        }

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "result_id": self.result_id,
            "grader_id": self.grader_id,
            "passed": self.passed,
            "score": self.score,
            "details": self.details,
            "created_at": self.created_at.isoformat()
        }
