from datetime import datetime, date
from enum import Enum
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    full_name: str


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    projects: List["Project"] = Relationship(back_populates="owner")


class ProjectBase(SQLModel):
    title: str
    description: Optional[str] = None


class Project(ProjectBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id")
    owner: Optional[User] = Relationship(back_populates="projects")
    tasks: List["Task"] = Relationship(back_populates="project")


class TagBase(SQLModel):
    name: str = Field(index=True, unique=True)


class TaskTagLink(SQLModel, table=True):
    task_id: Optional[int] = Field(default=None, foreign_key="task.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)
    relevance_score: int = Field(default=1, ge=1, le=10)


class Tag(TagBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tasks: List["Task"] = Relationship(back_populates="tags", link_model=TaskTagLink)


class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    priority: TaskPriority = TaskPriority.medium
    status: TaskStatus = TaskStatus.todo


class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    project: Optional[Project] = Relationship(back_populates="tasks")
    entries: List["TimeEntry"] = Relationship(back_populates="task")
    tags: List[Tag] = Relationship(back_populates="tasks", link_model=TaskTagLink)


class TimeEntryBase(SQLModel):
    started_at: datetime
    finished_at: datetime
    notes: Optional[str] = None


class TimeEntry(TimeEntryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id")
    spent_minutes: int = Field(ge=1)
    task: Optional[Task] = Relationship(back_populates="entries")


class DailyPlanBase(SQLModel):
    plan_date: date
    focus_notes: Optional[str] = None


class DailyPlan(DailyPlanBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
