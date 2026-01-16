"""
Evaluation service - orchestrates execution of test cases against agents
"""
from src.models.evaluation import EvaluationRun, EvaluationResult
from src.services.storage import StorageAbstraction
from src.services.agent_client import AgentClient
from src.services.test_case_service import TestCaseService
from src.services.grading_service import GradingService
from typing import List, Optional, Dict, Any
from datetime import datetime
import asyncio
import logging

logger = logging.getLogger(__name__)


class EvaluationService:
    """Service for managing evaluation runs"""

    def __init__(self, storage: StorageAbstraction, test_case_service: TestCaseService):
        self.storage = storage
        self.test_case_service = test_case_service
        self.agent_client = AgentClient(timeout=30)
        self.grading_service = GradingService(storage)

    def create_evaluation_run(
        self,
        test_case_ids: List[str],
        agent_endpoint_url: str,
        grader_ids: List[str]
    ) -> EvaluationRun:
        """Create a new evaluation run"""
        run = EvaluationRun(
            test_case_ids=test_case_ids,
            agent_endpoint_url=agent_endpoint_url,
            grader_ids=grader_ids,
            status="pending"
        )
        self.storage.create_evaluation_run(run.to_dict())
        logger.info(f"Created evaluation run {run.id}")
        return run

    def get_evaluation_run(self, run_id: str) -> Optional[EvaluationRun]:
        """Get an evaluation run by ID"""
        data = self.storage.get_evaluation_run(run_id)
        if not data:
            return None
        return EvaluationRun(**data)

    def list_evaluation_runs(self, skip: int = 0, limit: int = 10) -> List[EvaluationRun]:
        """List all evaluation runs with pagination"""
        data = self.storage.list_evaluation_runs(skip, limit)
        return [EvaluationRun(**item) for item in data]

    async def execute_evaluation(self, run_id: str) -> EvaluationRun:
        """
        Execute an evaluation run:
        1. Mark as running
        2. For each test case, call agent endpoint
        3. Store results
        4. Mark as completed
        """
        run = self.get_evaluation_run(run_id)
        if not run:
            raise ValueError(f"Evaluation run {run_id} not found")

        # Mark as running
        self.storage.update_evaluation_run(run_id, {
            "status": "running",
            "started_at": datetime.utcnow()
        })

        try:
            results_count = 0
            
            # Execute for each test case
            for test_case_id in run.test_case_ids:
                test_case = self.test_case_service.get_test_case(test_case_id)
                if not test_case:
                    logger.warning(f"Test case {test_case_id} not found")
                    continue

                # Call agent
                agent_result = await self.agent_client.call_agent(
                    run.agent_endpoint_url,
                    test_case.input
                )

                # Store result
                result = EvaluationResult(
                    run_id=run_id,
                    test_case_id=test_case_id,
                    agent_response=agent_result.get("response"),
                    response_latency_ms=agent_result.get("latency_ms"),
                    response_status=agent_result["status"],
                    error_message=agent_result.get("error")
                )
                self.storage.create_evaluation_result(result.to_dict())
                results_count += 1

            # Mark as completed
            self.storage.update_evaluation_run(run_id, {
                "status": "completed",
                "completed_at": datetime.utcnow(),
                "result_count": results_count
            })

            # Grade all results
            logger.info(f"Starting grading for run {run_id}")
            grading_metrics = await self.grading_service.grade_evaluation_run(run_id)
            logger.info(f"Grading metrics: {grading_metrics}")

            logger.info(f"Completed evaluation run {run_id} with {results_count} results")
            return self.get_evaluation_run(run_id)

        except Exception as e:
            # Mark as failed
            self.storage.update_evaluation_run(run_id, {
                "status": "failed",
                "error_message": str(e),
                "completed_at": datetime.utcnow()
            })
            logger.error(f"Evaluation run {run_id} failed: {e}")
            raise

    def get_evaluation_results(self, run_id: str) -> List[EvaluationResult]:
        """Get all results for an evaluation run"""
        data = self.storage.list_evaluation_results(run_id)
        return [EvaluationResult(**item) for item in data]

    async def start_evaluation_async(self, run_id: str):
        """Start evaluation in background (fire and forget)"""
        try:
            await self.execute_evaluation(run_id)
        except Exception as e:
            logger.error(f"Background evaluation failed: {e}")
