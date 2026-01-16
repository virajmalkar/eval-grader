"""
API response utilities and common patterns
"""
from typing import Any, Optional
from fastapi import HTTPException, status


def success_response(data: Any, message: str = "Success") -> dict:
    """Standard success response format"""
    return {
        "status": "success",
        "message": message,
        "data": data
    }


def error_response(
    message: str, 
    code: str = "INTERNAL_ERROR", 
    details: Optional[dict] = None
) -> dict:
    """Standard error response format"""
    response = {
        "status": "error",
        "message": message,
        "code": code,
    }
    if details:
        response["details"] = details
    return response


def raise_not_found(resource_type: str, resource_id: str):
    """Raise 404 Not Found error"""
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{resource_type} with id '{resource_id}' not found"
    )


def raise_bad_request(message: str, details: Optional[dict] = None):
    """Raise 400 Bad Request error"""
    detail = {"message": message}
    if details:
        detail.update(details)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail
    )


def raise_conflict(message: str):
    """Raise 409 Conflict error"""
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=message
    )
