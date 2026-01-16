"""
Grader service - list and get graders
"""
from src.models.grader import Grader
from src.graders.string_match import StringMatchGrader
from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

# Available graders (MVP only has string-match)
AVAILABLE_GRADERS = {
    "string-match": Grader(
        id="string-match",
        name="String Match",
        description="Case-insensitive string matching grader",
        type="string-match",
        config={
            "case_sensitive": False,
            "normalize_whitespace": False
        }
    )
}


class GraderService:
    """Service for managing graders"""

    @staticmethod
    def list_graders() -> List[Grader]:
        """List all available graders"""
        return list(AVAILABLE_GRADERS.values())

    @staticmethod
    def get_grader(grader_id: str) -> Optional[Grader]:
        """Get a grader by ID"""
        return AVAILABLE_GRADERS.get(grader_id)

    @staticmethod
    def get_grader_instance(grader_id: str) -> Optional[Any]:
        """Get an instantiated grader for execution"""
        if grader_id == "string-match":
            return StringMatchGrader()
        return None

    @staticmethod
    def validate_grader_ids(grader_ids: List[str]) -> bool:
        """Validate that all grader IDs are available"""
        for grader_id in grader_ids:
            if grader_id not in AVAILABLE_GRADERS:
                logger.warning(f"Unknown grader ID: {grader_id}")
                return False
        return True
