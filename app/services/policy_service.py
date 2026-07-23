from app.repositories.policy_repository import PolicyRepository


class PolicyService:

    def __init__(self):
        self.repository = PolicyRepository()

    async def get_all_policies(self) -> list[dict]:
        return await self.repository.find_all()

    async def get_policy(self, policy_id: str) -> dict | None:
        return await self.repository.find_by_id(policy_id)

    async def search_policies(
        self,
        policy_number: str | None,
        customer_name: str | None,
    ) -> list[dict]:

        return await self.repository.search(
            policy_number=policy_number,
            customer_name=customer_name,
        )
