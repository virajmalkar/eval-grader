"""
Mock agent server for testing evaluation runs
Responds to requests with sample responses for testing
"""
from fastapi import FastAPI, Request
import uvicorn
import asyncio

mock_app = FastAPI(title="Mock Agent Server")

# Sample responses for different inputs
MOCK_RESPONSES = {
    "What is the capital of France?": "Paris",
    "What is 2+2?": "4",
    "Say hello": "Hello!",
}


@mock_app.post("/evaluate")
async def evaluate(request: Request):
    """Simulate agent evaluation endpoint"""
    try:
        body = await request.json()
        input_text = body.get("input", "")
        
        # Simulate processing time
        await asyncio.sleep(0.1)
        
        # Return mock response
        response = MOCK_RESPONSES.get(input_text, f"Response to: {input_text}")
        
        return {
            "status": "success",
            "response": response,
            "model": "mock-model-v1"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


@mock_app.get("/health")
async def health():
    """Health check for mock agent"""
    return {"status": "healthy", "service": "mock-agent"}


if __name__ == "__main__":
    uvicorn.run(mock_app, host="localhost", port=9000)
