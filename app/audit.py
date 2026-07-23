import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class MockBlobStorage:

    STORAGE_DIR = Path("storage/audit")

    @classmethod
    def save(cls, audit_event: dict):
        cls.STORAGE_DIR.mkdir(parents=True, exist_ok=True)

        file_name = f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"

        file_path = cls.STORAGE_DIR / file_name

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(audit_event, f, indent=4)

        logger.info("Audit file saved: %s", file_path)


class MockServiceBus:

    @staticmethod
    def publish(event: dict):
        logger.info("Publishing audit event to Mock Service Bus")
        logger.info(event)


class AuditService:

    @staticmethod
    def audit(endpoint: str, payload: dict, status: str):

        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "endpoint": endpoint,
            "status": status,
            "request": payload,
        }

        MockBlobStorage.save(event)
        MockServiceBus.publish(event)
