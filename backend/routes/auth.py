from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Any
from jose import JWTError, jwt
from datetime import datetime, timedelta

from models.schemas import Token, EmployeeResponse
from config import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

MOCK_USERS = {
    "manager": {
        "password": "manager",
        "id": "00000000-0000-0000-0000-000000000010",
        "employee_code": "BM-04",
        "full_name": "Branch Manager",
        "email": "manager@bankguard.com",
        "role": "branch_manager",
        "branch_id": "00000000-0000-0000-0000-000000000001",
        "risk_score": 12.0,
    },
    "employee": {
        "password": "employee",
        "id": "00000000-0000-0000-0000-000000000011",
        "employee_code": "CS-18",
        "full_name": "Branch Employee",
        "email": "employee@bankguard.com",
        "role": "teller",
        "branch_id": "00000000-0000-0000-0000-000000000001",
        "risk_score": 21.0,
    },
    "admin": {
        "password": "admin",
        "id": "00000000-0000-0000-0000-000000000000",
        "employee_code": "ADM-01",
        "full_name": "Admin User",
        "email": "admin@bankguard.com",
        "role": "admin",
        "branch_id": "00000000-0000-0000-0000-000000000001",
        "risk_score": 0.0,
    },
}

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """Mock login for hackathon demo."""
    user = MOCK_USERS.get(form_data.username)
    if user and form_data.password == user["password"]:
        access_token = create_access_token(
            data={
                "sub": form_data.username,
                "role": user["role"],
                "branch_id": user["branch_id"],
            }
        )
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

@router.get("/me", response_model=EmployeeResponse)
async def read_users_me(token: str = Depends(oauth2_scheme)) -> Any:
    """Mock get current user."""
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
        username = payload.get("sub")
    except JWTError:
        raise credentials_exception

    user = MOCK_USERS.get(username)
    if not user:
        raise credentials_exception

    return {
        "id": user["id"],
        "employee_code": user["employee_code"],
        "full_name": user["full_name"],
        "email": user["email"],
        "role": user["role"],
        "branch_id": user["branch_id"],
        "is_active": True,
        "risk_score": user["risk_score"],
        "created_at": datetime.utcnow()
    }
