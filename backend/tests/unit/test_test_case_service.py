"""
Unit tests for TestCaseService
"""
import pytest
from src.services.test_case_service import TestCaseService
from src.services.storage_service import StorageService


@pytest.fixture
def service():
    """Create test service"""
    StorageService.reset_storage()
    storage = StorageService.get_storage()
    return TestCaseService(storage)


def test_create_test_case(service):
    """Test creating a test case"""
    test_case = service.create_test_case(
        input_text="What is 2+2?",
        expected_output="4"
    )
    assert test_case.id is not None
    assert test_case.input == "What is 2+2?"
    assert test_case.expected_output == "4"


def test_get_test_case(service):
    """Test getting a test case"""
    created = service.create_test_case(
        input_text="What is 2+2?",
        expected_output="4"
    )
    retrieved = service.get_test_case(created.id)
    assert retrieved is not None
    assert retrieved.id == created.id


def test_get_nonexistent_test_case(service):
    """Test getting a non-existent test case"""
    result = service.get_test_case("nonexistent")
    assert result is None


def test_list_test_cases(service):
    """Test listing test cases"""
    for i in range(3):
        service.create_test_case(
            input_text=f"Question {i}",
            expected_output=f"Answer {i}"
        )
    
    items = service.list_test_cases(skip=0, limit=10)
    assert len(items) == 3


def test_list_test_cases_pagination(service):
    """Test pagination of test cases"""
    for i in range(15):
        service.create_test_case(
            input_text=f"Question {i}",
            expected_output=f"Answer {i}"
        )
    
    page1 = service.list_test_cases(skip=0, limit=10)
    page2 = service.list_test_cases(skip=10, limit=10)
    
    assert len(page1) == 10
    assert len(page2) == 5


def test_update_test_case(service):
    """Test updating a test case"""
    created = service.create_test_case(
        input_text="Original",
        expected_output="Answer"
    )
    
    updated = service.update_test_case(
        created.id,
        input_text="Updated"
    )
    
    assert updated is not None
    assert updated.input == "Updated"


def test_delete_test_case(service):
    """Test deleting a test case"""
    created = service.create_test_case(
        input_text="To delete",
        expected_output="Answer"
    )
    
    result = service.delete_test_case(created.id)
    assert result is True
    
    retrieved = service.get_test_case(created.id)
    assert retrieved is None
