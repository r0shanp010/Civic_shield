import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.database import engine, Base, SessionLocal
from app.models.models import AdminUser
from app.utils.auth import get_password_hash
from app.routes import auth, complaints, admin

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Initialize database tables automatically
    Base.metadata.create_all(bind=engine)
    
    # 2. Seed default admin & officer credentials if table is empty
    db = SessionLocal()
    try:
        admin_exists = db.query(AdminUser).filter(AdminUser.username == "admin").first()
        if not admin_exists:
            # Seed super admin
            db_admin = AdminUser(
                username="admin",
                password_hash=get_password_hash("admin123"),
                role="Admin"
            )
            db.add(db_admin)
            
            # Seed an investigator officer
            db_officer = AdminUser(
                username="officer1",
                password_hash=get_password_hash("officer123"),
                role="Officer"
            )
            db.add(db_officer)
            db.commit()
            print("Successfully seeded default accounts in database: 'admin' (pass: admin123) and 'officer1' (pass: officer123)")
    except Exception as e:
        print(f"Error seeding database: {e}")
    finally:
        db.close()
        
    yield
    # Cleanup actions (if any) go here

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Secure whistleblower reporting platform utilizing NLP analytics.",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for Vite dev server or deployment domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount upload directory to make evidence attachments downloadable
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/api/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Attach APIRouters
app.include_router(auth.router)
app.include_router(complaints.router)
app.include_router(admin.router)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "CivicShield AI-Based Grievance Management System",
        "documentation": "/docs"
    }
