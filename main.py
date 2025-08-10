import uvicorn
from fastapi import FastAPI
from .api import router
from .es_client import ensure_index
from .config import settings

app = FastAPI(title="DeepResearch AI")
app.include_router(router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    ensure_index()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
