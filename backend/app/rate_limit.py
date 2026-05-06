from __future__ import annotations

from collections import defaultdict, deque
from time import monotonic

from fastapi import HTTPException, Request, status

_MAX_ATTEMPTS = 5
_WINDOW_SECONDS = 5 * 60
_attempts: dict[str, deque[float]] = defaultdict(deque)


def auth_rate_limit_key(request: Request, purpose: str, subject: str | int) -> str:
    client_host = request.client.host if request.client else "unknown"
    return f"{purpose}:{client_host}:{str(subject).strip().lower()}"


def check_auth_rate_limit(key: str) -> None:
    now = monotonic()
    attempts = _attempts[key]
    while attempts and now - attempts[0] > _WINDOW_SECONDS:
        attempts.popleft()
    if len(attempts) >= _MAX_ATTEMPTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many failed attempts. Try again later.",
        )


def record_auth_failure(key: str) -> None:
    check_auth_rate_limit(key)
    _attempts[key].append(monotonic())


def clear_auth_failures(key: str) -> None:
    _attempts.pop(key, None)


def reset_auth_rate_limits() -> None:
    _attempts.clear()
