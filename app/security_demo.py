import os

from fastapi import APIRouter, Query

router = APIRouter(prefix="/security-demo", tags=["Security Demo"])


@router.get("/command")
def execute_command(command: str = Query(...)):
    result = os.system(command)
    return {"exitCode": result}
