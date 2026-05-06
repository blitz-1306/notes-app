from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..auth import create_access_token, hash_password, verify_password
from ..deps import get_db
from ..models import User
from ..rate_limit import (
    auth_rate_limit_key,
    check_auth_rate_limit,
    clear_auth_failures,
    record_auth_failure,
)
from ..schemas import TokenOut, UserCreate, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(request: Request, payload: UserCreate, db: Session = Depends(get_db)) -> User:
    rate_limit_key = auth_rate_limit_key(request, "register", payload.username)
    check_auth_rate_limit(rate_limit_key)
    user = User(username=payload.username, password_hash=hash_password(payload.password))
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        record_auth_failure(rate_limit_key)
        raise HTTPException(status.HTTP_409_CONFLICT, "Username already exists") from None
    db.refresh(user)
    clear_auth_failures(rate_limit_key)
    return user


@router.post("/login", response_model=TokenOut)
def login(
    request: Request,
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> TokenOut:
    rate_limit_key = auth_rate_limit_key(request, "login", form.username)
    check_auth_rate_limit(rate_limit_key)
    user = db.query(User).filter(User.username == form.username).one_or_none()
    if user is None or not verify_password(form.password, user.password_hash):
        record_auth_failure(rate_limit_key)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid username or password")
    clear_auth_failures(rate_limit_key)
    token = create_access_token(user.id)
    return TokenOut(access_token=token)
