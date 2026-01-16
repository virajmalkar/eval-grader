"""
Grader model - Represents a pluggable grading implementation
"""
from pydantic import BaseModel, Field
from typing import Optional


class Grader(BaseModel):
    """Data model for graders"""
    id: str = Field(...)
    name: str = Field(...)
    description: str = Field(...)
    type: str = Field(...)
    config: Optional[dict] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "string-match",
                "name": "String Match",
                "description": "Case-insensitive string matching",
                "type": "string-match",
                "config": {
                    "case_sensitive": False,
                    "normalize_whitespace": False
                }
            }
        }

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "config": self.config
        }
