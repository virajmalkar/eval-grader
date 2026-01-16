"""
EvaluationRun and EvaluationResult models
"""
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from typing import Optional, List
import uuid


class EvaluationRun(BaseModel):
    """Data model for evaluation runs"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    test_case_ids: List[str] = Field(..., min_items=1)
    agent_endpoint_url: str = Field(...)
    grader_ids: List[str] = Field(..., min_items=1)
    status: str = Field(default="pending")  # pending, running, completed, failed
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result_count: int = Field(default=0)
    error_message: Optional[str] = Field(None, max_length=500)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440002",
                "test_case_ids": ["test-1", "test-2"],
                "agent_endpoint_url": "https://api.agent.example.com/evaluate",
                "grader_ids": ["string-match"],
                "status": "completed",
                "started_at": "2026-01-15T10:35:00Z",
                "completed_at": "2026-01-15T10:35:15Z",
                "result_count": 2,
                "error_message": None
            }
        }

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "test_case_ids": self.test_case_ids,
            "agent_endpoint_url": self.agent_endpoint_url,
            "grader_ids": self.grader_ids,
            "status": self.status,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "result_count": self.result_count,
            "error_message": self.error_message
        }


class EvaluationResult(BaseModel):
    """Data model for evaluation results"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    run_id: str = Field(...)
    test_case_id: str = Field(...)
    agent_response: Optional[str] = Field(None, max_length=10000)
    response_latency_ms: Optional[int] = Field(None, ge=0)
    response_status: str = Field(default="success")  # success, timeout, error
    error_message: Optional[str] = Field(None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440004",
                "run_id": "550e8400-e29b-41d4-a716-446655440002",
                "test_case_id": "550e8400-e29b-41d4-a716-446655440001",
                "agent_response": "Paris",
                "response_latency_ms": 245,
                "response_status": "success",
                "error_message": None,
                "created_at": "2026-01-15T10:35:01Z"
            }
        }

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "run_id": self.run_id,
            "test_case_id": self.test_case_id,
            "agent_response": self.agent_response,
            "response_latency_ms": self.response_latency_ms,
            "response_status": self.response_status,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat()
        }
