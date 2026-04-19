from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..deps import get_current_user, get_db
from ..models import Note, User

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("", response_model=list[str])
def list_tags(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[str]:
    rows = db.query(Note.tags).filter(Note.user_id == user.id).all()
    seen: set[str] = set()
    for (tags,) in rows:
        if tags:
            seen.update(tags)
    return sorted(seen)
