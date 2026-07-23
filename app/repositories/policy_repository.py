"""Repository responsible for communicating with Policy Admin."""

import logging
import time

import httpx

from app.exceptions import (
    DownstreamServiceError,
    DownstreamTimeoutError,
)

logger = logging.getLogger(__name__)


class PolicyRepository:

    BASE_URL = "http://127.0.0.1:8000"

    # Downstream Policy Admin gets only part of our total 3-second budget.
    DOWNSTREAM_TIMEOUT_SECONDS = 2.0

    # Log a warning before we actually reach the timeout.
    SLOW_CALL_THRESHOLD_SECONDS = 1.5

    async def find_all(self) -> list[dict]:

        # perf_counter() is designed for measuring elapsed time.
        start_time = time.perf_counter()

        try:
            timeout = httpx.Timeout(self.DOWNSTREAM_TIMEOUT_SECONDS)

            async with httpx.AsyncClient(timeout=timeout) as client:

                response = await client.get(
                    f"{self.BASE_URL}/mock-policy-admin/policies"
                )

                response.raise_for_status()

                return response.json()

        except httpx.TimeoutException as exc:

            logger.error(
                "Policy Admin request exceeded %.2f seconds",
                self.DOWNSTREAM_TIMEOUT_SECONDS,
            )

            # `raise ... from exc` preserves the original error,
            # which is extremely useful during troubleshooting.
            raise DownstreamTimeoutError("Policy Admin request timed out") from exc

        except httpx.HTTPError as exc:

            logger.exception("Policy Admin HTTP request failed")

            raise DownstreamServiceError("Policy Admin service unavailable") from exc

        finally:
            # finally executes whether the call succeeds OR fails.
            elapsed = time.perf_counter() - start_time

            if elapsed >= self.SLOW_CALL_THRESHOLD_SECONDS:
                logger.warning(
                    "Slow Policy Admin call detected: %.3f seconds",
                    elapsed,
                )
            else:
                logger.info(
                    "Policy Admin latency: %.3f seconds",
                    elapsed,
                )

    async def find_by_id(
        self,
        policy_id: str,
    ) -> dict | None:

        policies = await self.find_all()

        return next(
            (policy for policy in policies if policy["policyId"] == policy_id),
            None,
        )

    async def search(
        self,
        policy_number: str | None,
        customer_name: str | None,
    ) -> list[dict]:

        policies = await self.find_all()

        return [
            policy
            for policy in policies
            if (not policy_number or policy["policyNumber"] == policy_number)
            and (
                not customer_name
                or customer_name.lower() in policy["customerName"].lower()
            )
        ]
