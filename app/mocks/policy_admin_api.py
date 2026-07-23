"""
Mock downstream Policy Admin API.

In the real architecture this would be a separate backend system.
For this POC we expose it from the same FastAPI process so that we can
practice real HTTP integration without deploying another application.
"""

from fastapi import APIRouter

from app.mocks.policy_data import POLICIES

import asyncio

router = APIRouter(
    prefix="/mock-policy-admin",
    tags=["Mock Policy Admin"],
)


@router.get("/policies")
async def get_policies():
    """Simulate retrieving policies from the backend Policy Admin system."""

    """
    POC: simulate a slow downstream Policy Admin system.

    Our PolicyRepository has a 2-second HTTP timeout,
    so this 3-second delay should cause a timeout.
    """
    # await asyncio.sleep(3)
    return POLICIES
