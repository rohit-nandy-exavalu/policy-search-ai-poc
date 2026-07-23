import os

from fastapi import APIRouter, Query
from pathlib import Path

router = APIRouter(prefix="/security-demo", tags=["Security Demo"])


@router.get("/command")
def execute_command(command: str = Query(...)):
    result = os.system(command)
    return {"exitCode": result}


# Github actions didn't trigger in the previous commit


@router.get("/audit-file")
def get_audit_file(filename: str = Query(...)):
    file_path = Path("storage/audit") / filename

    with open(file_path, "r", encoding="utf-8") as file:
        return {"filename": filename, "content": file.read()}
