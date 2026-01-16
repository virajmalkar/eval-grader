"""
Test Cases API endpoints - CRUD operations
"""
from fastapi import APIRouter, Query, status
from src.api.schemas import TestCaseCreate, TestCaseUpdate, TestCaseResponse
from src.api.utils import success_response, raise_not_found
from src.services.storage_service import StorageService
from src.services.test_case_service import TestCaseService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/test-cases", tags=["test-cases"])

# Initialize service
_test_case_service: TestCaseService = None


def get_test_case_service() -> TestCaseService:
    """Get or create test case service"""
    global _test_case_service
    if _test_case_service is None:
        storage = StorageService.get_storage()
        _test_case_service = TestCaseService(storage)
    return _test_case_service


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_test_case(test_case: TestCaseCreate):
    """Create a new test case"""
    service = get_test_case_service()
    created = service.create_test_case(
        input_text=test_case.input,
        expected_output=test_case.expected_output,
        description=test_case.description,
        tags=test_case.tags
    )
    return success_response(
        TestCaseResponse(**created.to_dict()).__dict__,
        "Test case created"
    )


@router.get("/{test_case_id}")
async def get_test_case(test_case_id: str):
    """Get a test case by ID"""
    service = get_test_case_service()
    test_case = service.get_test_case(test_case_id)
    if not test_case:
        raise_not_found("TestCase", test_case_id)
    return success_response(TestCaseResponse(**test_case.to_dict()).__dict__)


@router.get("")
async def list_test_cases(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    """List test cases with pagination"""
    service = get_test_case_service()
    test_cases = service.list_test_cases(skip, limit)
    return success_response(
        [TestCaseResponse(**tc.to_dict()).__dict__ for tc in test_cases]
    )


@router.put("/{test_case_id}")
async def update_test_case(test_case_id: str, updates: TestCaseUpdate):
    """Update a test case"""
    service = get_test_case_service()
    updated = service.update_test_case(
        test_case_id,
        input_text=updates.input,
        expected_output=updates.expected_output,
        description=updates.description,
        tags=updates.tags
    )
    if not updated:
        raise_not_found("TestCase", test_case_id)
    return success_response(
        TestCaseResponse(**updated.to_dict()).__dict__,
        "Test case updated"
    )


@router.delete("/{test_case_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_test_case(test_case_id: str):
    """Delete a test case"""
    service = get_test_case_service()
    if not service.delete_test_case(test_case_id):
        raise_not_found("TestCase", test_case_id)
    return None
