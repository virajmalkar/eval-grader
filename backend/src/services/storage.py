"""
Storage abstraction layer - supports swapping implementations
"""
from typing import List, Optional, Dict, Any
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class StorageAbstraction(ABC):
    """Base class for storage implementations"""

    @abstractmethod
    def create_test_case(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Create a test case"""
        pass

    @abstractmethod
    def get_test_case(self, test_case_id: str) -> Optional[Dict[str, Any]]:
        """Get a test case by ID"""
        pass

    @abstractmethod
    def list_test_cases(self, skip: int = 0, limit: int = 10) -> List[Dict[str, Any]]:
        """List test cases with pagination"""
        pass

    @abstractmethod
    def update_test_case(self, test_case_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a test case"""
        pass

    @abstractmethod
    def delete_test_case(self, test_case_id: str) -> bool:
        """Delete a test case"""
        pass

    @abstractmethod
    def create_evaluation_run(self, run: Dict[str, Any]) -> Dict[str, Any]:
        """Create an evaluation run"""
        pass

    @abstractmethod
    def get_evaluation_run(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Get an evaluation run by ID"""
        pass

    @abstractmethod
    def list_evaluation_runs(self, skip: int = 0, limit: int = 10) -> List[Dict[str, Any]]:
        """List evaluation runs with pagination"""
        pass

    @abstractmethod
    def update_evaluation_run(self, run_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an evaluation run"""
        pass

    @abstractmethod
    def create_evaluation_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Create an evaluation result"""
        pass

    @abstractmethod
    def get_evaluation_result(self, result_id: str) -> Optional[Dict[str, Any]]:
        """Get an evaluation result by ID"""
        pass

    @abstractmethod
    def list_evaluation_results(self, run_id: str) -> List[Dict[str, Any]]:
        """List all results for a run"""
        pass

    @abstractmethod
    def create_score(self, score: Dict[str, Any]) -> Dict[str, Any]:
        """Create a score"""
        pass

    @abstractmethod
    def list_scores(self, result_id: str) -> List[Dict[str, Any]]:
        """List all scores for a result"""
        pass

    @abstractmethod
    def list_all_scores(self, run_id: str) -> List[Dict[str, Any]]:
        """List all scores for a run"""
        pass


class InMemoryStorage(StorageAbstraction):
    """In-memory storage implementation"""

    def __init__(self):
        self.test_cases: Dict[str, Dict[str, Any]] = {}
        self.evaluation_runs: Dict[str, Dict[str, Any]] = {}
        self.evaluation_results: Dict[str, Dict[str, Any]] = {}
        self.scores: Dict[str, List[Dict[str, Any]]] = {}
        logger.info("InMemoryStorage initialized")

    def create_test_case(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Create a test case"""
        self.test_cases[test_case["id"]] = test_case
        logger.debug(f"Created test case {test_case['id']}")
        return test_case

    def get_test_case(self, test_case_id: str) -> Optional[Dict[str, Any]]:
        """Get a test case by ID"""
        return self.test_cases.get(test_case_id)

    def list_test_cases(self, skip: int = 0, limit: int = 10) -> List[Dict[str, Any]]:
        """List test cases with pagination"""
        items = list(self.test_cases.values())
        return items[skip : skip + limit]

    def update_test_case(self, test_case_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a test case"""
        if test_case_id not in self.test_cases:
            return None
        self.test_cases[test_case_id].update(updates)
        logger.debug(f"Updated test case {test_case_id}")
        return self.test_cases[test_case_id]

    def delete_test_case(self, test_case_id: str) -> bool:
        """Delete a test case"""
        if test_case_id in self.test_cases:
            del self.test_cases[test_case_id]
            logger.debug(f"Deleted test case {test_case_id}")
            return True
        return False

    def create_evaluation_run(self, run: Dict[str, Any]) -> Dict[str, Any]:
        """Create an evaluation run"""
        self.evaluation_runs[run["id"]] = run
        logger.debug(f"Created evaluation run {run['id']}")
        return run

    def get_evaluation_run(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Get an evaluation run by ID"""
        return self.evaluation_runs.get(run_id)

    def list_evaluation_runs(self, skip: int = 0, limit: int = 10) -> List[Dict[str, Any]]:
        """List evaluation runs with pagination"""
        items = list(self.evaluation_runs.values())
        return items[skip : skip + limit]

    def update_evaluation_run(self, run_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an evaluation run"""
        if run_id not in self.evaluation_runs:
            return None
        self.evaluation_runs[run_id].update(updates)
        logger.debug(f"Updated evaluation run {run_id}")
        return self.evaluation_runs[run_id]

    def create_evaluation_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Create an evaluation result"""
        self.evaluation_results[result["id"]] = result
        logger.debug(f"Created evaluation result {result['id']}")
        return result

    def get_evaluation_result(self, result_id: str) -> Optional[Dict[str, Any]]:
        """Get an evaluation result by ID"""
        return self.evaluation_results.get(result_id)

    def list_evaluation_results(self, run_id: str) -> List[Dict[str, Any]]:
        """List all results for a run"""
        return [r for r in self.evaluation_results.values() if r["run_id"] == run_id]

    def create_score(self, score: Dict[str, Any]) -> Dict[str, Any]:
        """Create a score"""
        result_id = score["result_id"]
        if result_id not in self.scores:
            self.scores[result_id] = []
        self.scores[result_id].append(score)
        logger.debug(f"Created score {score['id']}")
        return score

    def list_scores(self, result_id: str) -> List[Dict[str, Any]]:
        """List all scores for a result"""
        return self.scores.get(result_id, [])

    def list_all_scores(self, run_id: str) -> List[Dict[str, Any]]:
        """List all scores for a run"""
        all_scores = []
        for result in self.evaluation_results.values():
            if result["run_id"] == run_id:
                all_scores.extend(self.list_scores(result["id"]))
        return all_scores
