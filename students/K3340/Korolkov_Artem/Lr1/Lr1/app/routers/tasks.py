from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db import get_session
from app.dependencies import get_current_user
from app.models import User, Task, Project, Tag, TaskTagLink
from app.schemas import TaskCreate, TaskUpdate, TaskWithRelations, TaskFull

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskWithRelations)
def create_task(
    payload: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> TaskWithRelations:
    project = session.get(Project, payload.project_id)
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found")
    task = Task.model_validate(payload)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.get("/{task_id}", response_model=TaskWithRelations)
def get_task(
    task_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
) -> TaskWithRelations:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/{task_id}/full", response_model=TaskFull)
def get_task_with_entries(
    task_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
) -> TaskFull:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskWithRelations)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
) -> TaskWithRelations:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session), _: User = Depends(get_current_user)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"ok": True}


@router.post("/{task_id}/tags/{tag_id}")
def add_tag_to_task(
    task_id: int,
    tag_id: int,
    relevance_score: int = 1,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    task = session.get(Task, task_id)
    tag = session.get(Tag, tag_id)
    if not task or not tag:
        raise HTTPException(status_code=404, detail="Task or tag not found")

    existing = session.exec(
        select(TaskTagLink).where(TaskTagLink.task_id == task_id, TaskTagLink.tag_id == tag_id)
    ).first()
    if existing:
        existing.relevance_score = relevance_score
        session.add(existing)
    else:
        session.add(TaskTagLink(task_id=task_id, tag_id=tag_id, relevance_score=relevance_score))
    session.commit()
    return {"status": "linked"}
