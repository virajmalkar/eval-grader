"""
Grader base interface - extensible grading system
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class GraderInterface(ABC):
    """Base interface for graders"""

    def __init__(self, grader_id: str, config: Optional[Dict[str, Any]] = None):
        self.grader_id = grader_id
        self.config = config or {}

    @abstractmethod
    def grade(self, agent_response: str, expected_output: str) -> Dict[str, Any]:
        """
        Grade a response against expected output

        Returns:
            {
                "passed": bool,
                "score": float (0.0-1.0),
                "details": dict with grading details
            }
        """
        pass

    @abstractmethod
    def validate_config(self) -> bool:
        """Validate grader configuration"""
        pass
