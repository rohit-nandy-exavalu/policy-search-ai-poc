"""FastAPI routes exposed by the Policy Search API."""

from fastapi import APIRouter, HTTPException

from app.models import PolicySearchRequest
from app.services.audit_service import AuditService
from app.services.policy_service import PolicyService

router = APIRouter(
    prefix="/policies",
    tags=["Policies"],
)

# Create our service once and reuse it across requests.
policy_service = PolicyService()


@router.get("")
async def get_all_policies():
    """Return all policies."""

    return await policy_service.get_all_policies()


@router.get("/{policy_id}")
async def get_policy(policy_id: str):
    """Retrieve one policy using its internal policy ID."""

    policy = await policy_service.get_policy(policy_id)

    if policy is None:
        raise HTTPException(
            status_code=404,
            detail="Policy not found",
        )

    return policy


@router.post("/search")
async def search_policies(request: PolicySearchRequest):
    """Search policies using one or more optional criteria."""

    results = await policy_service.search_policies(
        policy_number=request.policyNumber,
        customer_name=request.customerName,
    )

    AuditService.audit(
        endpoint="/policies/search",
        payload=request.model_dump(),
        status="SUCCESS",
    )

    return results
