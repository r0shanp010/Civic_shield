import os
import random
import string
import uuid
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Complaint, Evidence, AIPrediction, ComplaintUpdate, User
from app.schemas.schemas import ComplaintCreate, ComplaintPublicResponse
from app.ai.classifier import ai_service
from app.config import settings
from app.utils.auth import get_current_citizen

router = APIRouter(prefix="/api/complaints", tags=["Public Complaints"])

# Allowed extensions and size limits
ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png", ".docx"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

def generate_tracking_id() -> str:
    """Generates a unique tracking ID in the format COR-YYYY-XXXXXX"""
    year = datetime.now().year
    chars = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"COR-{year}-{chars}"

@router.post("", status_code=status.HTTP_201_CREATED)
def create_complaint(
    request: Request,
    description: str = Form(...),
    category: str = Form(None),
    department: str = Form(None),
    location: str = Form(None),
    incident_date: str = Form(None),
    amount_involved: float = Form(None),
    db: Session = Depends(get_db)
):
    """
    Submits a new anonymous or authenticated complaint and triggers modular AI classification/analysis.
    """
    # 0. Check optional authorization to link registered citizen
    user_id = None
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            import jwt
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username = payload.get("sub")
            role = payload.get("role")
            if role == "Citizen":
                citizen = db.query(User).filter(User.username == username).first()
                if citizen:
                    user_id = citizen.id
        except Exception as e:
            print(f"Optional citizen auth linking skipped: {e}")
    parsed_date = None
    if incident_date:
        try:
            parsed_date = datetime.strptime(incident_date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid incident_date format. Must be YYYY-MM-DD")

    # Generate unique tracking ID
    tracking_id = generate_tracking_id()
    while db.query(Complaint).filter(Complaint.tracking_id == tracking_id).first() is not None:
        tracking_id = generate_tracking_id()

    # Create the complaint record
    db_complaint = Complaint(
        tracking_id=tracking_id,
        description=description,
        category=category,
        department=department,
        location=location,
        incident_date=parsed_date,
        amount_involved=amount_involved,
        status="Pending",
        priority="Medium",
        user_id=user_id
    )
    
    db.add(db_complaint)
    db.commit()
    db.refresh(db_complaint)

    # 1. Add initial progress update
    initial_update = ComplaintUpdate(
        complaint_id=db_complaint.id,
        status="Pending",
        previous_status=None,
        note="Complaint submitted. Tracking ID generated and assigned to review queue.",
        internal_note="Case file initialized. Raw complaint description and evidence mapped to database records. Queue status set to Pending.",
        citizen_update="Complaint received successfully. Unique tracking key generated. Assigned to the pending queue for review.",
        updated_by="System"
    )
    db.add(initial_update)
    db.commit()

    # 2. Perform AI predictions
    try:
        # Fetch previous complaints for duplicate checks
        previous_records = []
        all_comps = db.query(Complaint).filter(Complaint.id != db_complaint.id).all()
        for c in all_comps:
            previous_records.append({
                "id": c.id,
                "description": c.description
            })

        # Run analysis
        ai_res = ai_service.analyze_complaint(
            description=description,
            amount_involved=amount_involved,
            previous_complaints=previous_records
        )

        # Store prediction results
        db_ai_pred = AIPrediction(
            complaint_id=db_complaint.id,
            predicted_category=ai_res["predicted_category"],
            category_confidence=ai_res["category_confidence"],
            predicted_priority=ai_res["predicted_priority"],
            priority_confidence=ai_res["priority_confidence"],
            recommended_department=ai_res["recommended_department"],
            department_confidence=ai_res["department_confidence"],
            duplicate_score=ai_res["duplicate_score"],
            suspicious_flag=ai_res["suspicious_flag"]
        )
        db.add(db_ai_pred)
        
        # Update priority if recommended by AI
        db_complaint.priority = ai_res["predicted_priority"]
        
        # 3. Add AI Triage complete progress update
        ai_update = ComplaintUpdate(
            complaint_id=db_complaint.id,
            status="Pending",
            previous_status="Pending",
            note="AI analysis completed.",
            internal_note=f"AI prediction completed. Category: {ai_res['predicted_category']} ({ai_res['category_confidence']:.1f}%), Priority: {ai_res['predicted_priority']} ({ai_res['priority_confidence']:.1f}%), Dept: {ai_res['recommended_department']} ({ai_res['department_confidence']:.1f}%).",
            citizen_update="AI triage complete. Initial category categorization and routing completed.",
            updated_by="System"
        )
        db.add(ai_update)
        db.commit()
        
    except Exception as e:
        print(f"Error during AI analysis execution: {e}")
        # Insert a placeholder prediction if anything fails, ensuring transaction completeness
        placeholder_pred = AIPrediction(
            complaint_id=db_complaint.id,
            predicted_category=category or "Misuse of Authority",
            category_confidence=50.0,
            predicted_priority="Medium",
            priority_confidence=50.0,
            recommended_department=department or "Police",
            department_confidence=50.0,
            duplicate_score=0.0,
            suspicious_flag=False
        )
        db.add(placeholder_pred)
        db.commit()

    return {
        "message": "Complaint submitted successfully.",
        "tracking_id": tracking_id
    }


@router.post("/{tracking_id}/evidence", status_code=status.HTTP_201_CREATED)
async def upload_evidence(
    tracking_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Uploads supporting evidence documents (PDF, JPG, PNG, DOCX) up to 10MB for an existing complaint.
    """
    complaint = db.query(Complaint).filter(Complaint.tracking_id == tracking_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Validate file size (reading chunk by chunk to check size limit)
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File exceeds maximum size limit of {MAX_FILE_SIZE / (1024*1024)}MB."
        )

    # Ensure uploads folder exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    # Save file with unique randomized filename
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    
    with open(file_path, "wb") as f:
        f.write(contents)

    # Store file record in database
    db_evidence = Evidence(
        complaint_id=complaint.id,
        file_name=file.filename,
        file_type=file_ext,
        file_path=file_path
    )
    db.add(db_evidence)
    db.commit()

    return {
        "message": "Evidence uploaded successfully",
        "file_name": file.filename
    }


@router.get("/{tracking_id}", response_model=ComplaintPublicResponse)
def get_complaint_status(tracking_id: str, db: Session = Depends(get_db)):
    """
    Returns public-safe progress and verification logs for tracking complaints anonymously.
    Excludes sensitive fields like AI metrics, admin investigations, and officer notes.
    """
    complaint = db.query(Complaint).filter(Complaint.tracking_id == tracking_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
        
    return complaint

@router.get("/my/list", response_model=List[ComplaintPublicResponse])
def get_my_complaints(
    db: Session = Depends(get_db), 
    current_citizen: User = Depends(get_current_citizen)
):
    """
    Returns a list of all complaints submitted by the authenticated citizen.
    """
    return db.query(Complaint).filter(Complaint.user_id == current_citizen.id).all()
