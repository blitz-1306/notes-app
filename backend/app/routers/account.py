from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..auth import hash_password, verify_password
from ..deps import get_current_user, get_db
from ..models import User
from ..schemas import ChangePasswordIn, DeleteAccountIn, OkOut

router = APIRouter(prefix="/account", tags=["account"])


@router.post("/change-password", response_model=OkOut)
def change_password(
    payload: ChangePasswordIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> OkOut:
    if not verify_password(payload.current_password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Current password is wrong")
    user.password_hash = hash_password(payload.new_password)
    db.commit()
    return OkOut()


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    payload: DeleteAccountIn,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Password is wrong")
    db.delete(user)
    db.commit()
