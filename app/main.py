from fastapi import FastAPI
from app.routes import router
app=FastAPI(title='Policy Search AI POC')
app.include_router(router)
@app.get('/health')
def health():
    return {'status':'UP'}
