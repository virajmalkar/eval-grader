"""
TestCase service - CRUD operations for test cases
"""
from src.models.test_case import TestCase
from src.services.storage import StorageAbstraction
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class TestCaseService:
    """Service for managing test cases"""

    def __init__(self, storage: StorageAbstraction):
        self.storage = storage

    def create_test_case(
        self, 
        input_text: str, 
        expected_output: str,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> TestCase:
        """Create a new test case"""
        test_case = TestCase(
            input=input_text,
            expected_output=expected_output,
            description=description,
            tags=tags or []
        )
        test_case.validate_constraints()
        
        self.storage.create_test_case(test_case.to_dict())
        logger.info(f"Created test case {test_case.id}")
        return test_case

    def get_test_case(self, test_case_id: str) -> Optional[TestCase]:
        """Get a test case by ID"""
        data = self.storage.get_test_case(test_case_id)
        if not data:
            return None
        return TestCase(**data)

    def list_test_cases(self, skip: int = 0, limit: int = 10) -> List[TestCase]:
        """List all test cases with pagination"""
        data = self.storage.list_test_cases(skip, limit)
        return [TestCase(**item) for item in data]

    def update_test_case(
        self,
        test_case_id: str,
        input_text: Optional[str] = None,
        expected_output: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Optional[TestCase]:
        """Update a test case"""
        existing = self.get_test_case(test_case_id)
        if not existing:
            return None

        updates = {}
        if input_text is not None:
            updates["input"] = input_text
        if expected_output is not None:
            updates["expected_output"] = expected_output
        if description is not None:
            updates["description"] = description
        if tags is not None:
            updates["tags"] = tags
        
        updates["modified_at"] = datetime.utcnow()

        data = self.storage.update_test_case(test_case_id, updates)
        if not data:
            return None
        
        test_case = TestCase(**data)
        test_case.validate_constraints()
        logger.info(f"Updated test case {test_case_id}")
        return test_case

    def delete_test_case(self, test_case_id: str) -> bool:
        """Delete a test case"""
        result = self.storage.delete_test_case(test_case_id)
        if result:
            logger.info(f"Deleted test case {test_case_id}")
        return result

    def get_test_cases_by_ids(self, test_case_ids: List[str]) -> List[TestCase]:
        """Get multiple test cases by IDs"""
        test_cases = []
        for tc_id in test_case_ids:
            tc = self.get_test_case(tc_id)
            if tc:
                test_cases.append(tc)
        return test_cases
