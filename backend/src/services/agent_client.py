"""
Agent HTTP client - calls external agent endpoints
"""
import httpx
import logging
from typing import Optional, Dict, Any
from datetime import datetime
import time

logger = logging.getLogger(__name__)

# Default timeout for agent calls (30 seconds)
DEFAULT_AGENT_TIMEOUT = 30


class AgentClient:
    """HTTP client for calling agent endpoints"""

    def __init__(self, timeout: int = DEFAULT_AGENT_TIMEOUT):
        self.timeout = timeout

    async def call_agent(
        self, 
        endpoint_url: str, 
        input_text: str
    ) -> Dict[str, Any]:
        """
        Call an agent endpoint with input

        Returns:
            {
                "status": "success" | "timeout" | "error",
                "response": str (if success),
                "latency_ms": int,
                "error": str (if error)
            }
        """
        start_time = time.time()
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    endpoint_url,
                    json={"input": input_text}
                )
                response.raise_for_status()
                
                data = response.json()
                latency_ms = int((time.time() - start_time) * 1000)
                
                logger.debug(f"Agent call successful to {endpoint_url} in {latency_ms}ms")
                
                return {
                    "status": "success",
                    "response": data.get("response", ""),
                    "latency_ms": latency_ms
                }
        
        except httpx.TimeoutException:
            latency_ms = int((time.time() - start_time) * 1000)
            logger.warning(f"Agent timeout after {latency_ms}ms")
            return {
                "status": "timeout",
                "latency_ms": latency_ms,
                "error": f"Agent did not respond within {self.timeout} seconds"
            }
        
        except httpx.HTTPError as e:
            latency_ms = int((time.time() - start_time) * 1000)
            error_msg = str(e)
            logger.error(f"Agent HTTP error: {error_msg}")
            return {
                "status": "error",
                "latency_ms": latency_ms,
                "error": error_msg
            }
        
        except Exception as e:
            latency_ms = int((time.time() - start_time) * 1000)
            error_msg = str(e)
            logger.error(f"Unexpected agent error: {error_msg}")
            return {
                "status": "error",
                "latency_ms": latency_ms,
                "error": error_msg
            }
