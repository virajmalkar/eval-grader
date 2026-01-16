"""
Pydantic request/response schemas for API contracts
"""
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime


# ============= Test Case Schemas =============

class TestCaseCreate(BaseModel):
    """Schema for creating a test case"""
    input: str = Field(..., min_length=1, max_length=10000)
    expected_output: str = Field(..., min_length=1, max_length=10000)
    description: Optional[str] = Field(None, max_length=500)
    tags: Optional[List[str]] = Field(None, max_items=10)

    class Config:
        json_schema_extra = {
            "example": {
                "input": "What is the capital of France?",
                "expected_output": "Paris",
                "description": "Basic geography question",
                "tags": ["geography", "basic"]
            }
        }


class TestCaseUpdate(BaseModel):
    """Schema for updating a test case"""
    input: Optional[str] = Field(None, min_length=1, max_length=10000)
    expected_output: Optional[str] = Field(None, min_length=1, max_length=10000)
    description: Optional[str] = Field(None, max_length=500)
    tags: Optional[List[str]] = Field(None, max_items=10)


class TestCaseResponse(BaseModel):
    """Schema for test case response"""
    id: str
    input: str
    expected_output: str
    description: Optional[str]
    tags: Optional[List[str]]
    created_at: datetime
    modified_at: datetime


# ============= Evaluation Run Schemas =============

class EvaluationRunCreate(BaseModel):
    """Schema for creating an evaluation run"""
    test_case_ids: List[str] = Field(..., min_items=1)
    agent_endpoint_url: HttpUrl
    grader_ids: List[str] = Field(..., min_items=1)

    class Config:
        json_schema_extra = {
            "example": {
                "test_case_ids": ["test-1", "test-2"],
                "agent_endpoint_url": "https://api.agent.example.com/evaluate",
                "grader_ids": ["string-match"]
            }
        }


class EvaluationRunResponse(BaseModel):
    """Schema for evaluation run response"""
    id: str
    test_case_ids: List[str]
    agent_endpoint_url: str
    grader_ids: List[str]
    status: str  # pending, running, completed, failed
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    result_count: int
    error_message: Optional[str]


# ============= Evaluation Result Schemas =============

class EvaluationResultResponse(BaseModel):
    """Schema for evaluation result response"""
    id: str
    run_id: str
    test_case_id: str
    agent_response: Optional[str]
    response_latency_ms: Optional[int]
    response_status: str  # success, timeout, error
    error_message: Optional[str]
    created_at: datetime


# ============= Grader Schemas =============

class GraderResponse(BaseModel):
    """Schema for grader response"""
    id: str
    name: str
    description: str
    type: str


class ScoreResponse(BaseModel):
    """Schema for score response"""
    id: str
    result_id: str
    grader_id: str
    passed: bool
    score: Optional[float]
    details: Optional[dict]


# ============= Error Schemas =============

class ErrorResponse(BaseModel):
    """Schema for error responses"""
    status: str = "error"
    message: str
    code: str
    details: Optional[dict] = None
