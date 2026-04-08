from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db import get_session
from app.dependencies import get_current_user
from app.models import User, Project
from app.schemas import ProjectCreate, ProjectRead, ProjectWithTasks

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectRead)
def create_project(
    payload: ProjectCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> ProjectRead:
    project = Project(**payload.model_dump(), owner_id=current_user.id)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@router.get("/", response_model=list[ProjectRead])
def list_projects(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> list[ProjectRead]:
    return session.exec(select(Project).where(Project.owner_id == current_user.id)).all()


@router.get("/{project_id}/with-tasks", response_model=ProjectWithTasks)
def project_with_tasks(
    project_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> ProjectWithTasks:
    project = session.get(Project, project_id)
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    project = session.get(Project, project_id)
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found")
    session.delete(project)
    session.commit()
    return {"ok": True}
