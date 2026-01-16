"""
Backend configuration from environment variables
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Server configuration
HOST = os.getenv("BACKEND_HOST", "localhost")
PORT = int(os.getenv("BACKEND_PORT", "8000"))

# Agent configuration
AGENT_TIMEOUT = int(os.getenv("AGENT_TIMEOUT", "30"))

# Grader configuration
GRADER_TIMEOUT = int(os.getenv("GRADER_TIMEOUT", "5"))

# Testing
TESTING = os.getenv("TESTING", "false").lower() == "true"
