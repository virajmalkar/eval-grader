"""
TestCase model - Represents a single evaluation scenario
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
import uuid


class TestCase(BaseModel):
    """Data model for test cases"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    input: str = Field(..., min_length=1, max_length=10000)
    expected_output: str = Field(..., min_length=1, max_length=10000)
    description: Optional[str] = Field(None, max_length=500)
    tags: Optional[List[str]] = Field(None, max_items=10)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    modified_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "input": "What is the capital of France?",
                "expected_output": "Paris",
                "description": "Basic geography question",
                "tags": ["geography", "basic"],
                "created_at": "2026-01-15T10:30:00Z",
                "modified_at": "2026-01-15T10:30:00Z"
            }
        }

    def validate_constraints(self) -> None:
        """Validate test case constraints"""
        if self.modified_at < self.created_at:
            raise ValueError("modified_at cannot be before created_at")

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "input": self.input,
            "expected_output": self.expected_output,
            "description": self.description,
            "tags": self.tags or [],
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat()
        }
