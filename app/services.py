from app.mock_data import POLICIES

def get_all(): return POLICIES

def get_by_id(pid): return next((p for p in POLICIES if p['policyId']==pid),None)

def search(req):
 return [p for p in POLICIES if (not req.policyNumber or p['policyNumber']==req.policyNumber) and (not req.customerName or req.customerName.lower() in p['customerName'].lower())]
