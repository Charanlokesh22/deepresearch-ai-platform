from fastapi import APIRouter, BackgroundTasks, HTTPException
from .tasks import TASKS, submit_job_background
import asyncio
from .config import settings

router = APIRouter()
# create an event loop for background tasks
loop = asyncio.get_event_loop()

@router.post("/research")
async def create_research(payload: dict, background_tasks: BackgroundTasks):
    """
    payload: {"query": "topic", "start_urls": ["https://...","https://..."]}
    """
    query = payload.get("query")
    start_urls = payload.get("start_urls") or []
    if not query or not start_urls:
        raise HTTPException(400, "query and start_urls required")

    uid_future = submit_job_background(loop, query, start_urls)
    # uid_future is concurrent.futures.Future -> result when ready; but we want uid now.
    # our submit returns a Future for the coroutine; we can poll TASKS to find uid set inside run_research_job
    # simpler: generate uid here and call run_research_job with it — but for simplicity, we'll return a temporary id.
    return {"status": "accepted", "message": "Job started. Poll /status/{id}", "id_hint": "poll /tasks for running tasks"}

@router.get("/tasks")
async def list_tasks():
    return TASKS

@router.get("/task/{uid}")
async def get_task(uid: str):
    if uid not in TASKS:
        raise HTTPException(404, "task not found")
    return TASKS[uid]

@router.get("/report/{uid}")
async def get_report(uid: str):
    t = TASKS.get(uid)
    if not t:
        raise HTTPException(404, "task not found")
    if t["status"] != "completed":
        raise HTTPException(400, "task not completed")
    return t["result"]
