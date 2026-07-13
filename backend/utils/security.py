"""
BankGuard Enterprise — Security Utilities.

Provides JWT token management, password hashing, and FastAPI dependency
factories for authentication and role-based access control.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Annotated, Callable, List, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

try:
    from passlib.context import CryptContext
except ImportError:
    CryptContext = None

from config import settings
from models.schemas import TokenData

# ── Password hashing ────────────────────────────────────────────────────

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") if CryptContext else None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_password_hash(password: str) -> str:
    """Return a bcrypt hash for the given plaintext *password*."""
    if pwd_context is None:
        raise RuntimeError("passlib is required for password hashing")
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify *plain_password* against a bcrypt *hashed_password*."""
    if pwd_context is None:
        raise RuntimeError("passlib is required for password verification")
    return pwd_context.verify(plain_password, hashed_password)


# ── JWT helpers ──────────────────────────────────────────────────────────


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Create a signed JWT access token.

    Parameters
    ----------
    data:
        Payload to encode (must include ``sub`` claim).
    expires_delta:
        Custom token lifetime.  Falls back to
        ``settings.ACCESS_TOKEN_EXPIRE_MINUTES`` when *None*.

    Returns
    -------
    str
        Encoded JWT string.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta
        or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )


def verify_token(token: str) -> TokenData:
    """
    Decode and validate a JWT token.

    Raises
    ------
    HTTPException (401)
        If the token is invalid or missing required claims.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        username: Optional[str] = payload.get("sub")
        role: Optional[str] = payload.get("role")
        if username is None:
            raise credentials_exception
        return TokenData(username=username, role=role)
    except JWTError:
        raise credentials_exception


# ── FastAPI dependencies ─────────────────────────────────────────────────


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> TokenData:
    """
    FastAPI dependency — extract and validate the current user from
    the ``Authorization: Bearer <token>`` header.
    """
    return verify_token(token)


def require_role(allowed_roles: List[str]) -> Callable:
    """
    Dependency factory that restricts access to users whose JWT ``role``
    claim is in *allowed_roles*.

    Usage::

        @router.get("/admin-only", dependencies=[Depends(require_role(["admin"]))])
        async def admin_endpoint(): ...
    """

    async def _role_checker(
        current_user: Annotated[TokenData, Depends(get_current_user)],
    ) -> TokenData:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{current_user.role}' is not authorised for this resource",
            )
        return current_user

    return _role_checker
