from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import uvicorn
import logging

from routes import alerts, auth, loans, swift
from services.scheduler import DataCleanupScheduler

logger = logging.getLogger(__name__)

tags_metadata = [
    {
        "name": "Authentication",
        "description": "Demo login and current-user endpoints. Use admin/admin to get a bearer token.",
    },
    {
        "name": "Alerts",
        "description": "Fraud and behavioral-risk alert endpoints.",
    },
    {
        "name": "Loans",
        "description": "Loan application intake and risk scoring endpoints.",
    },
    {
        "name": "SWIFT",
        "description": "SWIFT message ingestion and CBS reconciliation endpoints.",
    },
    {
        "name": "Health",
        "description": "Service status endpoints.",
    },
]

app = FastAPI(
    title="BankGuard Enterprise API",
    description=(
        "Backend API for the Behavioral Threat & Fraud Detection Platform.\n\n"
        "Swagger UI is available at `/api/docs`. Authenticate with the demo "
        "credentials `admin` / `admin` from the Authorize button."
    ),
    version="1.0.0",
    openapi_tags=tags_metadata,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,
        "displayRequestDuration": True,
        "filter": True,
        "persistAuthorization": True,
        "tryItOutEnabled": True,
    },
)

# Configure CORS for the frontend SPA
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Startup / Shutdown Handlers ──────────────────────────────────────

@app.on_event("startup")
async def startup():
    """Initialize database and start background tasks on app startup."""
    try:
        from init_db import init_database
        
        init_database()
        logger.info("✓ Database initialized")
    except Exception as exc:
        logger.error(f"Database initialization failed: {exc}")

    try:
        DataCleanupScheduler.start()
        logger.info("✓ Background cleanup scheduler started")
    except Exception as exc:
        logger.error(f"Failed to start scheduler: {exc}")


@app.on_event("shutdown")
async def shutdown():
    """Stop background tasks on app shutdown."""
    DataCleanupScheduler.stop()
    logger.info("✓ Background cleanup scheduler stopped")

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["Alerts"])
app.include_router(loans.router, prefix="/api/v1/loans", tags=["Loans"])
app.include_router(swift.router, prefix="/api/v1/swift", tags=["SWIFT"])

@app.get("/", include_in_schema=False)
def root():
    return {
        "service": "BankGuard Enterprise API",
        "swagger_ui": "/api/docs",
        "openapi_schema": "/api/openapi.json",
        "health": "/api/v1/health",
    }

@app.get("/docs", include_in_schema=False)
def swagger_redirect():
    return RedirectResponse(url="/api/docs")

@app.get("/api/v1/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "BankGuard Enterprise API"}

@app.get("/api/v1/health/dependencies", tags=["Health"])
def dependency_health_check():
    checks = {
        "postgres": {"configured": True, "ok": False},
        "mongo": {"configured": False, "ok": False},
    }

    try:
        from config import settings
        from db import check_mongo, check_postgres

        checks["postgres"]["ok"] = check_postgres()
        checks["mongo"]["configured"] = bool(settings.MONGODB_URI)
        checks["mongo"]["ok"] = check_mongo() if settings.MONGODB_URI else False
    except Exception as exc:
        return {
            "status": "degraded",
            "checks": checks,
            "detail": str(exc),
        }

    status = "ok" if checks["postgres"]["ok"] else "degraded"
    return {"status": status, "checks": checks}

# ── Data Lifecycle Management ────────────────────────────────────────

@app.post("/api/v1/data/employees/{employee_id}/set-expiration", tags=["Health"])
def set_employee_expiration(employee_id: str, ttl_minutes: int = 30):
    """
    Set a 30-minute expiration on employee data.
    After expiration, the record will be archived to MongoDB and deleted.
    
    - **employee_id**: Employee UUID
    - **ttl_minutes**: Time-to-live in minutes (default: 30)
    """
    from services.data_lifecycle import DataLifecycleService
    
    try:
        from uuid import UUID
        emp_uuid = UUID(employee_id)
        DataLifecycleService.set_expiration_on_employee(emp_uuid, ttl_minutes)
        return {
            "status": "ok",
            "message": f"Employee {employee_id} will expire in {ttl_minutes} minutes",
            "ttl_minutes": ttl_minutes,
        }
    except Exception as exc:
        return {"status": "error", "detail": str(exc)}, 400


@app.get("/api/v1/data/employees/{employee_id}/expiration-status", tags=["Health"])
def get_employee_expiration_status(employee_id: str):
    """
    Get the expiration status for an employee.
    Returns remaining TTL in seconds and expiration timestamp.
    """
    from services.data_lifecycle import DataLifecycleService
    
    try:
        from uuid import UUID
        emp_uuid = UUID(employee_id)
        status = DataLifecycleService.get_expiration_status(emp_uuid)
        
        if status is None:
            return {
                "status": "not_expiring",
                "message": "Employee has no expiration set",
            }
        
        return {"status": "expiring", "expiration": status}
    except Exception as exc:
        return {"status": "error", "detail": str(exc)}, 400


@app.post("/api/v1/data/cleanup", tags=["Health"])
def trigger_cleanup():
    """
    Manually trigger the cleanup of expired employees.
    Normally runs automatically every 5 minutes.
    """
    from services.data_lifecycle import DataLifecycleService
    
    try:
        deleted = DataLifecycleService.delete_expired_employees()
        return {
            "status": "ok",
            "message": f"Cleaned up {deleted} expired employee records",
            "deleted_count": deleted,
        }
    except Exception as exc:
        return {"status": "error", "detail": str(exc)}, 500

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
