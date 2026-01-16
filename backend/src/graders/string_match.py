"""
String-Match grader - MVP implementation
"""
from .base import GraderInterface
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class StringMatchGrader(GraderInterface):
    """
    String-match grader for MVP

    Config:
    {
        "case_sensitive": bool (default False),
        "normalize_whitespace": bool (default False)
    }
    """

    def __init__(self, grader_id: str = "string-match", config: Optional[Dict[str, Any]] = None):
        super().__init__(grader_id, config)
        self.case_sensitive = self.config.get("case_sensitive", False)
        self.normalize_whitespace = self.config.get("normalize_whitespace", False)

    def validate_config(self) -> bool:
        """Validate configuration"""
        for key in self.config:
            if key not in ["case_sensitive", "normalize_whitespace"]:
                logger.warning(f"Unknown config key: {key}")
        return True

    def _normalize(self, text: str) -> str:
        """Apply normalization rules to text"""
        if self.normalize_whitespace:
            text = " ".join(text.split())

        if not self.case_sensitive:
            text = text.lower()

        return text

    def grade(self, agent_response: str, expected_output: str) -> Dict[str, Any]:
        """
        Grade response using string matching

        Returns:
            {
                "passed": bool,
                "score": 1.0 if passed else 0.0,
                "details": {
                    "expected": normalized_expected,
                    "actual": normalized_actual,
                    "match": "exact" or "mismatch"
                }
            }
        """
        # Normalize both strings
        normalized_expected = self._normalize(expected_output)
        normalized_actual = self._normalize(agent_response)

        # Check for exact match
        passed = normalized_expected == normalized_actual
        score = 1.0 if passed else 0.0

        return {
            "passed": passed,
            "score": score,
            "details": {
                "expected": normalized_expected,
                "actual": normalized_actual,
                "match": "exact" if passed else "mismatch"
            }
        }
