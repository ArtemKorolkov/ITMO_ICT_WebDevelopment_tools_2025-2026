from datetime import datetime, date
from typing import Optional, List
from sqlmodel import SQLModel

from app.models import TaskPriority, TaskStatus


class UserCreate(SQLModel):
    username: str
    email: str
    full_name: str
    password: str


class UserRead(SQLModel):
    id: int
    username: str
    email: str
    full_name: str
    is_active: bool


class PasswordChange(SQLModel):
    old_password: str
    new_password: str


class LoginRequest(SQLModel):
    username: str
    password: str


class TokenResponse(SQLModel):
    access_token: str
    token_type: str = "bearer"


class ProjectCreate(SQLModel):
    title: str
    description: Optional[str] = None


class ProjectRead(ProjectCreate):
    id: int
    owner_id: int


class TagCreate(SQLModel):
    name: str


class TagRead(TagCreate):
    id: int


class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    priority: TaskPriority = TaskPriority.medium
    status: TaskStatus = TaskStatus.todo
    project_id: int


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None


class TimeEntryCreate(SQLModel):
    started_at: datetime
    finished_at: datetime
    notes: Optional[str] = None


class DailyPlanCreate(SQLModel):
    plan_date: date
    focus_notes: Optional[str] = None


class TaskWithRelations(SQLModel):
    id: int
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    priority: TaskPriority
    status: TaskStatus
    project_id: int
    tags: List[TagRead] = []


class TimeEntryRead(SQLModel):
    id: int
    started_at: datetime
    finished_at: datetime
    spent_minutes: int
    notes: Optional[str] = None


class TaskFull(TaskWithRelations):
    entries: List[TimeEntryRead] = []


class ProjectWithTasks(ProjectRead):
    tasks: List[TaskWithRelations] = []
