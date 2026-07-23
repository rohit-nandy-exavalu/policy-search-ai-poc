from fastapi import APIRouter,HTTPException
from app.models import PolicySearchRequest
from app import services
router=APIRouter(prefix='/policies',tags=['Policies'])
@router.get('')
def all_policies(): return services.get_all()
@router.get('/{policy_id}')
def by_id(policy_id:str):
 p=services.get_by_id(policy_id)
 if not p: raise HTTPException(status_code=404,detail='Policy not found')
 return p
@router.post('/search')
def search(req:PolicySearchRequest): return services.search(req)
