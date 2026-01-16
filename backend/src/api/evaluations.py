"""
Evaluation API endpoints - run management and execution
"""
from fastapi import APIRouter, Query, BackgroundTasks, status
from src.api.schemas import EvaluationRunCreate, EvaluationRunResponse, EvaluationResultResponse
from src.api.utils import success_response, raise_not_found
from src.services.storage_service import StorageService
from src.services.test_case_service import TestCaseService
from src.services.evaluation_service import EvaluationService
from src.services.grader_service import GraderService
import asyncio
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/evaluations", tags=["evaluations"])

# Initialize services
_evaluation_service: EvaluationService = None
_test_case_service: TestCaseService = None


def get_evaluation_service() -> EvaluationService:
    """Get or create evaluation service"""
    global _evaluation_service, _test_case_service
    if _evaluation_service is None:
        storage = StorageService.get_storage()
        _test_case_service = TestCaseService(storage)
        _evaluation_service = EvaluationService(storage, _test_case_service)
    return _evaluation_service


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_evaluation(run: EvaluationRunCreate, background_tasks: BackgroundTasks):
    """Create and start a new evaluation run"""
    service = get_evaluation_service()
    
    # Validate graders
    if not GraderService.validate_grader_ids(run.grader_ids):
        return {"status": "error", "message": "Invalid grader IDs"}, 400

    # Create run
    created_run = service.create_evaluation_run(
        test_case_ids=run.test_case_ids,
        agent_endpoint_url=str(run.agent_endpoint_url),
        grader_ids=run.grader_ids
    )

    # Start execution in background
    background_tasks.add_task(service.execute_evaluation, created_run.id)

    return success_response(
        EvaluationRunResponse(**created_run.to_dict()).__dict__,
        "Evaluation run created and started"
    )


@router.get("/{run_id}")
async def get_evaluation_status(run_id: str):
    """Get evaluation run status"""
    service = get_evaluation_service()
    run = service.get_evaluation_run(run_id)
    if not run:
        raise_not_found("EvaluationRun", run_id)
    return success_response(EvaluationRunResponse(**run.to_dict()).__dict__)


@router.get("")
async def list_evaluations(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    """List evaluation runs with pagination"""
    service = get_evaluation_service()
    runs = service.list_evaluation_runs(skip, limit)
    return success_response(
        [EvaluationRunResponse(**r.to_dict()).__dict__ for r in runs]
    )


@router.get("/{run_id}/results")
async def get_evaluation_results(run_id: str):
    """Get all results for an evaluation run"""
    service = get_evaluation_service()
    
    # Verify run exists
    run = service.get_evaluation_run(run_id)
    if not run:
        raise_not_found("EvaluationRun", run_id)

    # Get results
    results = service.get_evaluation_results(run_id)
    
    # Calculate summary stats
    total_results = len(results)
    successful_results = sum(1 for r in results if r.response_status == "success")
    failed_results = sum(1 for r in results if r.response_status == "error")
    timeout_results = sum(1 for r in results if r.response_status == "timeout")
    
    avg_latency = (
        sum(r.response_latency_ms for r in results if r.response_latency_ms) / successful_results
        if successful_results > 0 else 0
    )

    # Get grading results with scores
    results_with_scores = []
    for result in results:
        result_dict = EvaluationResultResponse(**result.to_dict()).__dict__
        # Get scores for this result
        scores = service.storage.list_scores(result.id)
        result_dict["scores"] = scores
        results_with_scores.append(result_dict)

    return success_response({
        "results": results_with_scores,
        "summary": {
            "total": total_results,
            "successful": successful_results,
            "failed": failed_results,
            "timeout": timeout_results,
            "avg_latency_ms": round(avg_latency, 2)
        }
    })
