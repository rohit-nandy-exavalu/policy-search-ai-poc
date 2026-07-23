from pydantic import BaseModel
class PolicySearchRequest(BaseModel):
    policyNumber:str|None=None
    customerName:str|None=None
