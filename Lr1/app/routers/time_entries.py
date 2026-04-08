from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db import get_session
from app.dependencies import get_current_user
from app.models import User, Task, TimeEntry
from app.schemas import TimeEntryCreate

router = APIRouter(prefix="/tasks/{task_id}/time-entries", tags=["TimeEntries"])


@router.post("/")
def create_entry(
    task_id: int,
    payload: TimeEntryCreate,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    minutes = int((payload.finished_at - payload.started_at).total_seconds() // 60)
    if minutes <= 0:
        raise HTTPException(status_code=400, detail="Finished time must be after started time")

    entry = TimeEntry(
        task_id=task_id,
        started_at=payload.started_at,
        finished_at=payload.finished_at,
        spent_minutes=minutes,
        notes=payload.notes,
    )
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry
