"""
Graders API endpoints - list available graders
"""
from fastapi import APIRouter
from src.api.schemas import GraderResponse
from src.api.utils import success_response, raise_not_found
from src.services.grader_service import GraderService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/graders", tags=["graders"])


@router.get("")
async def list_graders():
    """List all available graders"""
    graders = GraderService.list_graders()
    return success_response(
        [GraderResponse(**g.to_dict()).__dict__ for g in graders]
    )


@router.get("/{grader_id}")
async def get_grader(grader_id: str):
    """Get grader details by ID"""
    grader = GraderService.get_grader(grader_id)
    if not grader:
        raise_not_found("Grader", grader_id)
    return success_response(GraderResponse(**grader.to_dict()).__dict__)
