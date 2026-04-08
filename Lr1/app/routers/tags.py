from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db import get_session
from app.dependencies import get_current_user
from app.models import Tag, User
from app.schemas import TagCreate, TagRead

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.post("/", response_model=TagRead)
def create_tag(
    payload: TagCreate,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
) -> TagRead:
    existing = session.exec(select(Tag).where(Tag.name == payload.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tag already exists")
    tag = Tag.model_validate(payload)
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag


@router.get("/", response_model=list[TagRead])
def list_tags(session: Session = Depends(get_session), _: User = Depends(get_current_user)) -> list[TagRead]:
    return session.exec(select(Tag)).all()
