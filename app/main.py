"""Application entry point."""

import logging

from fastapi import FastAPI

from app.routes import router as policy_router
from app.security_demo import router as security_demo_router
from app.mocks.policy_admin_api import router as mock_policy_admin_router

from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions import (
    DownstreamServiceError,
    DownstreamTimeoutError,
)

# Central logging configuration.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s : %(message)s",
)


app = FastAPI(
    title="Policy Search API",
    version="1.0.0",
    description="Mule to Azure migration security and performance POC",
)


# Production-style Policy API.
app.include_router(policy_router)

# Isolated endpoints used only for CodeQL experiments.
app.include_router(security_demo_router)

# GET /mock-policy-admin/policies
app.include_router(mock_policy_admin_router)


@app.get("/health", tags=["Health"])
def health():
    """Simple health endpoint for availability checks."""

    return {
        "status": "UP",
        "service": "policy-search-api",
    }


@app.exception_handler(DownstreamTimeoutError)
async def downstream_timeout_handler(
    request: Request,
    exc: DownstreamTimeoutError,
):
    """Return a consistent response when Policy Admin times out."""

    return JSONResponse(
        status_code=504,
        content={
            "error": "DOWNSTREAM_TIMEOUT",
            "message": str(exc),
        },
    )


@app.exception_handler(DownstreamServiceError)
async def downstream_service_handler(
    request: Request,
    exc: DownstreamServiceError,
):
    """Return a consistent response when Policy Admin is unavailable."""

    return JSONResponse(
        status_code=502,
        content={
            "error": "DOWNSTREAM_SERVICE_ERROR",
            "message": str(exc),
        },
    )


# Client
#   │
#   ▼
# FastAPI Route
#   │
#   ▼
# Policy Service
#   │
#   ▼
# Repository
#   │
#   ├── latency measurement
#   ├── 2 sec timeout
#   ├── HTTP error handling
#   │
#   ▼
# Policy Admin
