"""
Grading service - applies graders to evaluation results
Per-result isolation: grader failures don't cascade
"""
from src.models.score import Score
from src.services.storage import StorageAbstraction
from src.services.grader_service import GraderService
from typing import List, Dict, Any
from datetime import datetime
import asyncio
import logging

logger = logging.getLogger(__name__)

# Default grader timeout
GRADER_TIMEOUT = 5


class GradingService:
    """Service for grading evaluation results"""

    def __init__(self, storage: StorageAbstraction):
        self.storage = storage

    async def grade_evaluation_run(self, run_id: str) -> Dict[str, Any]:
        """
        Grade all results in an evaluation run

        Returns metrics about grading success/failure
        """
        # Get all results for this run
        results = self.storage.list_evaluation_results(run_id)
        
        grading_metrics = {
            "total_results": len(results),
            "total_scores": 0,
            "successful_scores": 0,
            "failed_scores": 0,
            "errors": []
        }

        # For each result, apply each grader
        for result in results:
            # Only grade successful agent responses
            if result["response_status"] != "success":
                logger.debug(f"Skipping grading for non-success result {result['id']}")
                continue

            # Get the evaluation run to find graders
            run = self.storage.get_evaluation_run(run_id)
            if not run:
                continue

            agent_response = result.get("agent_response", "")

            # Get test case for expected output
            test_case_id = result["test_case_id"]
            test_case = self.storage.test_cases.get(test_case_id) if hasattr(self.storage, 'test_cases') else None

            if not test_case:
                logger.warning(f"Test case {test_case_id} not found for grading")
                continue

            expected_output = test_case.get("expected_output", "")

            # Apply each grader to this result
            for grader_id in run.get("grader_ids", []):
                try:
                    score = await self._grade_with_grader(
                        grader_id,
                        result["id"],
                        agent_response,
                        expected_output
                    )
                    if score:
                        self.storage.create_score(score.to_dict())
                        grading_metrics["total_scores"] += 1
                        grading_metrics["successful_scores"] += 1

                except Exception as e:
                    # Per-result isolation: capture error but don't stop
                    error_msg = f"Grader {grader_id} failed on result {result['id']}: {str(e)}"
                    logger.warning(error_msg)
                    grading_metrics["failed_scores"] += 1
                    grading_metrics["errors"].append(error_msg)

        logger.info(f"Grading completed for run {run_id}: {grading_metrics}")
        return grading_metrics

    async def _grade_with_grader(
        self,
        grader_id: str,
        result_id: str,
        agent_response: str,
        expected_output: str
    ) -> Score:
        """
        Apply a single grader to a result with timeout

        Returns Score object
        """
        try:
            # Get grader instance with timeout
            grader = GraderService.get_grader_instance(grader_id)
            if not grader:
                raise ValueError(f"Grader {grader_id} not found")

            # Execute grader with timeout
            grading_result = await asyncio.wait_for(
                asyncio.to_thread(grader.grade, agent_response, expected_output),
                timeout=GRADER_TIMEOUT
            )

            # Create score from grading result
            score = Score(
                result_id=result_id,
                grader_id=grader_id,
                passed=grading_result["passed"],
                score=grading_result["score"],
                details=grading_result.get("details")
            )

            return score

        except asyncio.TimeoutError:
            logger.warning(f"Grader {grader_id} timed out after {GRADER_TIMEOUT}s")
            raise
        except Exception as e:
            logger.error(f"Error grading with {grader_id}: {e}")
            raise

    def get_grading_results(self, run_id: str) -> Dict[str, Any]:
        """Get grading results summary for a run"""
        all_scores = self.storage.list_all_scores(run_id)

        summary = {
            "total_scores": len(all_scores),
            "passed": sum(1 for s in all_scores if s.get("passed")),
            "failed": sum(1 for s in all_scores if not s.get("passed")),
            "by_grader": {}
        }

        # Group by grader
        for score in all_scores:
            grader_id = score.get("grader_id")
            if grader_id not in summary["by_grader"]:
                summary["by_grader"][grader_id] = {
                    "total": 0,
                    "passed": 0,
                    "failed": 0
                }
            
            summary["by_grader"][grader_id]["total"] += 1
            if score.get("passed"):
                summary["by_grader"][grader_id]["passed"] += 1
            else:
                summary["by_grader"][grader_id]["failed"] += 1

        return summary
