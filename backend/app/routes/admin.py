from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import (
    Complaint, Evidence, AIPrediction, ComplaintUpdate, 
    AdminUser, Assignment, AuditLog, CaseAction
)
from app.schemas.schemas import (
    ComplaintAdminResponse, DashboardStats, AnalyticsResponse,
    ChartDataPoint, TrendDataPoint, AssignmentCreate, ComplaintUpdateCreate,
    ConfirmAdvance, TransitionUnderReview, TransitionAssign, TransitionInvestigate,
    TransitionResolve, TransitionClose, AddCaseAction
)
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/admin", tags=["Admin Grievance Operations"])

@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard_stats(
    db: Session = Depends(get_db), 
    current_user: AdminUser = Depends(get_current_user)
):
    """
    Returns card metrics for high-level admin dashboard views.
    """
    total = db.query(Complaint).count()
    pending = db.query(Complaint).filter(Complaint.status == "Pending").count()
    investigation = db.query(Complaint).filter(
        Complaint.status.in_(["Assigned", "Investigating", "Under Review"])
    ).count()
    resolved = db.query(Complaint).filter(
        Complaint.status.in_(["Resolved", "Closed", "Action Taken"])
    ).count()
    
    high = db.query(Complaint).filter(Complaint.priority == "High").count()
    critical = db.query(Complaint).filter(Complaint.priority == "Critical").count()
    
    # AI Specific flags
    duplicate = db.query(Complaint).join(AIPrediction).filter(
        AIPrediction.duplicate_score >= 50.0
    ).count()
    suspicious = db.query(Complaint).join(AIPrediction).filter(
        AIPrediction.suspicious_flag == True
    ).count()

    return {
        "total_complaints": total,
        "pending_complaints": pending,
        "under_investigation": investigation,
        "resolved_complaints": resolved,
        "high_priority": high,
        "critical_priority": critical,
        "duplicate_flags": duplicate,
        "suspicious_flags": suspicious
    }


@router.get("/complaints", response_model=List[ComplaintAdminResponse])
def list_complaints(
    category: Optional[str] = None,
    department: Optional[str] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None,
    duplicate_flag: Optional[bool] = None,
    suspicious_flag: Optional[bool] = None,
    search: Optional[str] = None,
    sort_by: str = "created_at",
    sort_dir: str = "desc",
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    """
    Query, filter, and search through submitted complaints. Fully paginated and queryable.
    """
    query = db.query(Complaint)
    
    # 1. Applying static column filters
    if category:
        query = query.filter(Complaint.category == category)
    if department:
        query = query.filter(Complaint.department == department)
    if priority:
        query = query.filter(Complaint.priority == priority)
    if status:
        query = query.filter(Complaint.status == status)
        
    # 2. Applying AI prediction flag filters
    if duplicate_flag is not None or suspicious_flag is not None:
        query = query.join(AIPrediction)
        if duplicate_flag is not None:
            if duplicate_flag:
                query = query.filter(AIPrediction.duplicate_score >= 50.0)
            else:
                query = query.filter(AIPrediction.duplicate_score < 50.0)
        if suspicious_flag is not None:
            query = query.filter(AIPrediction.suspicious_flag == suspicious_flag)

    # 3. Applying string searches
    if search:
        query = query.filter(
            or_(
                Complaint.description.like(f"%{search}%"),
                Complaint.tracking_id.like(f"%{search}%"),
                Complaint.location.like(f"%{search}%")
            )
        )
        
    # 4. Sorting
    sort_column = getattr(Complaint, sort_by, Complaint.created_at)
    if sort_dir == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # 5. Pagination offset
    offset = (page - 1) * limit
    return query.offset(offset).limit(limit).all()


@router.get("/complaints/{id}", response_model=ComplaintAdminResponse)
def get_complaint(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: AdminUser = Depends(get_current_user)
):
    """
    Retrieve comprehensive details, AI evaluations, file attachments, and notes for a complaint.
    """
    complaint = db.query(Complaint).filter(Complaint.id == id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint


@router.put("/complaints/{id}/status")
def update_complaint_status(
    id: int,
    payload: ComplaintUpdateCreate,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    """
    Allows authorized administrators to update the complaint state and attach manual progress notes.
    """
    complaint = db.query(Complaint).filter(Complaint.id == id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    # Update Complaint Status
    complaint.status = payload.status
    db.commit()

    # Append History Timeline Update
    new_update = ComplaintUpdate(
        complaint_id=complaint.id,
        status=payload.status,
        note=payload.note,
        updated_by=current_user.username
    )
    db.add(new_update)

    # Log action to audit logs
    audit = AuditLog(
        user_id=current_user.id,
        action=f"Updated status to '{payload.status}' with note: '{payload.note[:50]}...'",
        complaint_id=complaint.id
    )
    db.add(audit)
    db.commit()

    return {"message": "Complaint status updated successfully"}


STATUS_SEQUENCE = ["Pending", "Under Review", "Assigned", "Investigating", "Resolved", "Closed"]

@router.post("/complaints/{id}/request-advance")
def request_status_advance(
    id: int,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    """
    Computes the next logical status step and generates a 6-digit OTP code for citizen confirmation.
    """
    import random
    complaint = db.query(Complaint).filter(Complaint.id == id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
        
    current_status = complaint.status
    if current_status not in STATUS_SEQUENCE:
        raise HTTPException(status_code=400, detail=f"Invalid current status: {current_status}")
        
    current_idx = STATUS_SEQUENCE.index(current_status)
    if current_idx >= len(STATUS_SEQUENCE) - 1:
        raise HTTPException(status_code=400, detail="Complaint is already closed and cannot be advanced further.")
        
    next_status = STATUS_SEQUENCE[current_idx + 1]
    
    # Generate 6-digit verification code
    code = f"{random.randint(100000, 999999)}"
    
    complaint.next_status = next_status
    complaint.verification_code = code
    db.commit()
    
    print(f"\n[SECURITY DESK] Generated citizen OTP code {code} for status advancement to {next_status}\n")
    
    return {
        "message": f"Verification code generated for status advancement to {next_status}",
        "next_status": next_status,
        "verification_code": code
    }

@router.post("/complaints/{id}/confirm-advance")
def confirm_status_advance(
    id: int,
    payload: ConfirmAdvance,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    """
    Validates the 6-digit citizen OTP and advances the case status step.
    """
    complaint = db.query(Complaint).filter(Complaint.id == id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
        
    if not complaint.verification_code:
        raise HTTPException(status_code=400, detail="No status advancement request is pending for this complaint.")
        
    if payload.code != complaint.verification_code:
        raise HTTPException(status_code=400, detail="Incorrect citizen authorization code. Verification failed.")
        
    old_status = complaint.status
    new_status = complaint.next_status
    
    # Save status updates
    complaint.status = new_status
    complaint.verification_code = None
    complaint.next_status = None
    
    # Append History Timeline Update
    new_update = ComplaintUpdate(
        complaint_id=complaint.id,
        status=new_status,
        note=payload.note,
        updated_by=current_user.username
    )
    db.add(new_update)
    
    # Audit log
    audit = AuditLog(
        user_id=current_user.id,
        action=f"Advanced status from '{old_status}' to '{new_status}' with code verification.",
        complaint_id=complaint.id
    )
    db.add(audit)
    db.commit()
    
    return {
        "message": f"Complaint advanced to {new_status} successfully.",
        "status": new_status
    }


@router.put("/complaints/{id}/assign")
def assign_complaint(
    id: int,
    payload: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    """
    Assigns a complaint to an active officer/department.
    """
    complaint = db.query(Complaint).filter(Complaint.id == id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    # Update status to Assigned
    complaint.status = "Assigned"
    
    # Store Assignment record
    new_assign = Assignment(
        complaint_id=complaint.id,
        assigned_department=payload.assigned_department,
        assigned_officer=payload.assigned_officer
    )
    db.add(new_assign)

    # Insert status update log
    officer_name = payload.assigned_officer if payload.assigned_officer else "Unassigned Officer"
    note = f"Complaint assigned to department '{payload.assigned_department}' (Officer: {officer_name})."
    
    new_update = ComplaintUpdate(
        complaint_id=complaint.id,
        status="Assigned",
        note=note,
        updated_by=current_user.username
    )
    db.add(new_update)

    # Audit logging
    audit = AuditLog(
        user_id=current_user.id,
        action=f"Assigned complaint to {payload.assigned_department} / {officer_name}",
        complaint_id=complaint.id
    )
    db.add(audit)
    
    db.commit()
    return {"message": f"Complaint successfully assigned to {payload.assigned_department}"}


@router.get("/analytics", response_model=AnalyticsResponse)
def get_analytics(
    db: Session = Depends(get_db), 
    current_user: AdminUser = Depends(get_current_user)
):
    """
    Aggregates statistical breakdown charts (department, priority, category) and trendlines.
    """
    # 1. Department counts
    dept_counts = db.query(
        Complaint.department, func.count(Complaint.id)
    ).group_by(Complaint.department).all()
    by_department = [
        ChartDataPoint(name=str(d[0]) if d[0] else "Unassigned", value=int(d[1]))
        for d in dept_counts
    ]

    # 2. Category counts
    cat_counts = db.query(
        Complaint.category, func.count(Complaint.id)
    ).group_by(Complaint.category).all()
    by_category = [
        ChartDataPoint(name=str(c[0]) if c[0] else "Other", value=int(c[1]))
        for c in cat_counts
    ]

    # 3. Priority counts
    prio_counts = db.query(
        Complaint.priority, func.count(Complaint.id)
    ).group_by(Complaint.priority).all()
    by_priority = [
        ChartDataPoint(name=str(p[0]), value=int(p[1]))
        for p in prio_counts
    ]

    # 4. Monthly trends (using SQLite/MySQL formatted groupings)
    # Simple extraction of Year-Month
    is_sqlite = db.bind.url.drivername.startswith("sqlite")
    if is_sqlite:
        trend_query = db.query(
            func.strftime("%Y-%m", Complaint.created_at).label("month"),
            func.count(Complaint.id)
        ).group_by("month").order_by("month").all()
    else:
        trend_query = db.query(
            func.date_format(Complaint.created_at, "%Y-%m").label("month"),
            func.count(Complaint.id)
        ).group_by("month").order_by("month").all()
        
    monthly_trends = [
        TrendDataPoint(date=str(t[0]), count=int(t[1]))
        for t in trend_query
    ]

    # 5. Resolution rate
    total = db.query(Complaint).count()
    resolved = db.query(Complaint).filter(
        Complaint.status.in_(["Resolved", "Closed", "Action Taken"])
    ).count()
    
    resolution_rate = (resolved / total) * 100.0 if total > 0 else 0.0

    return {
        "by_department": by_department,
        "by_category": by_category,
        "by_priority": by_priority,
        "monthly_trends": monthly_trends,
        "resolution_rate": round(resolution_rate, 2)
    }


# --- Verified Case Journey Transitions ---

@router.post("/complaints/{id}/transition/under-review")
def transition_to_under_review(
    id: int,
    payload: TransitionUnderReview,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    complaint = db.query(Complaint).filter(Complaint.id == id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
        
    old_status = complaint.status
    if not payload.override and old_status != "Pending":
        raise HTTPException(
            status_code=400, 
            detail=f"This case must complete the current processing stage before advancing. Expected: Pending, Current: {old_status}"
        )
        
    # Update category / priority
    if payload.category:
        complaint.category = payload.category
    if payload.priority:
        complaint.priority = payload.priority
        
    complaint.status = "Under Review"
    db.commit()
    
    # Save update
    new_update = ComplaintUpdate(
        complaint_id=complaint.id,
        status="Under Review",
        previous_status=old_status,
        note=payload.internal_note[:100],
        internal_note=payload.internal_note,
        citizen_update=payload.citizen_update,
        updated_by=current_user.username
    )
    db.add(new_update)
    
    # Log Audit
    action_text = f"Advanced status to Under Review."
    if payload.override:
        action_text = f"[OVERRIDE ESCALATION] Bypassed sequence to advance to Under Review."
    audit = AuditLog(
        user_id=current_user.id,
        action=action_text,
        complaint_id=complaint.id
    )
    db.add(audit)
    db.commit()
    
    return {"message": "Case is now Under Review.", "status": "Under Review"}

@router.post("/complaints/{id}/transition/assign")
def transition_to_assigned(
    id: int,
    payload: TransitionAssign,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    complaint = db.query(Complaint).filter(Complaint.id == id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
        
    old_status = complaint.status
    if not payload.override and old_status != "Under Review":
        raise HTTPException(
            status_code=400, 
            detail=f"This case must complete the current processing stage before advancing. Expected: Under Review, Current: {old_status}"
        )
        
    # Record audit log check if admin changed recommended department
    ai_reco_dept = complaint.ai_prediction.recommended_department if complaint.ai_prediction else None
    dept_change_note = ""
    if ai_reco_dept and ai_reco_dept != payload.department:
        dept_change_note = f" (Admin override: AI recommended '{ai_reco_dept}', but admin assigned '{payload.department}')"
        
    complaint.department = payload.department
    complaint.status = "Assigned"
    
    # Create or update Assignment
    assign_rec = db.query(Assignment).filter(Assignment.complaint_id == complaint.id).first()
    if assign_rec:
        assign_rec.assigned_department = payload.department
    else:
        assign_rec = Assignment(
            complaint_id=complaint.id,
            assigned_department=payload.department
        )
        db.add(assign_rec)
        
    # Insert Approved Case Actions
    for action_desc in payload.approved_actions:
        new_act = CaseAction(
            complaint_id=complaint.id,
            action_type="Required Investigation Procedure",
            action_description=action_desc,
            suggested_by_ai=True
        )
        db.add(new_act)
        
    db.commit()
    
    # Save update
    new_update = ComplaintUpdate(
        complaint_id=complaint.id,
        status="Assigned",
        previous_status=old_status,
        note=payload.internal_note[:100],
        internal_note=payload.internal_note + dept_change_note,
        citizen_update=payload.citizen_update,
        updated_by=current_user.username
    )
    db.add(new_update)
    
    # Log Audit
    action_text = f"Assigned case to department '{payload.department}'" + dept_change_note
    if payload.override:
        action_text = f"[OVERRIDE ESCALATION] Bypassed sequence to Assign to '{payload.department}'"
    audit = AuditLog(
        user_id=current_user.id,
        action=action_text,
        complaint_id=complaint.id
    )
    db.add(audit)
    db.commit()
    
    return {"message": f"Case assigned to {payload.department}.", "status": "Assigned"}

@router.post("/complaints/{id}/transition/investigate")
def transition_to_investigate(
    id: int,
    payload: TransitionInvestigate,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    complaint = db.query(Complaint).filter(Complaint.id == id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
        
    old_status = complaint.status
    if not payload.override and old_status != "Assigned":
        raise HTTPException(
            status_code=400, 
            detail=f"This case must complete the current processing stage before advancing. Expected: Assigned, Current: {old_status}"
        )
        
    complaint.status = "Investigating"
    
    # Update Assignment
    assign_rec = db.query(Assignment).filter(Assignment.complaint_id == complaint.id).first()
    if assign_rec:
        assign_rec.assigned_officer = payload.officer
    else:
        assign_rec = Assignment(
            complaint_id=complaint.id,
            assigned_department=complaint.department or "Other",
            assigned_officer=payload.officer
        )
        db.add(assign_rec)
        
    db.commit()
    
    # Save update
    new_update = ComplaintUpdate(
        complaint_id=complaint.id,
        status="Investigating",
        previous_status=old_status,
        note=payload.internal_note[:100],
        internal_note=payload.internal_note,
        citizen_update=payload.citizen_update,
        updated_by=current_user.username
    )
    db.add(new_update)
    
    # Log Audit
    action_text = f"Assigned case to officer '{payload.officer}' and started investigation."
    if payload.override:
        action_text = f"[OVERRIDE ESCALATION] Bypassed sequence to Investigating. Assigned officer '{payload.officer}'."
    audit = AuditLog(
        user_id=current_user.id,
        action=action_text,
        complaint_id=complaint.id
    )
    db.add(audit)
    db.commit()
    
    return {"message": f"Investigation started by {payload.officer}.", "status": "Investigating"}

@router.post("/complaints/{id}/transition/resolve")
def transition_to_resolved(
    id: int,
    payload: TransitionResolve,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    complaint = db.query(Complaint).filter(Complaint.id == id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
        
    old_status = complaint.status
    if not payload.override and old_status != "Investigating":
        raise HTTPException(
            status_code=400, 
            detail=f"This case must complete the current processing stage before advancing. Expected: Investigating, Current: {old_status}"
        )
        
    complaint.status = "Resolved"
    db.commit()
    
    # Save update
    combined_internal = f"Resolution Type: {payload.resolution_type}\nSummary: {payload.resolution_summary}\nInternal Notes: {payload.internal_note}"
    new_update = ComplaintUpdate(
        complaint_id=complaint.id,
        status="Resolved",
        previous_status=old_status,
        note=payload.internal_note[:100],
        internal_note=combined_internal,
        citizen_update=payload.citizen_update,
        updated_by=current_user.username
    )
    db.add(new_update)
    
    # Log Audit
    action_text = f"Marked complaint as Resolved. Resolution: {payload.resolution_type}."
    if payload.override:
        action_text = f"[OVERRIDE ESCALATION] Bypassed sequence to Resolved."
    audit = AuditLog(
        user_id=current_user.id,
        action=action_text,
        complaint_id=complaint.id
    )
    db.add(audit)
    db.commit()
    
    return {"message": "Case marked as Resolved.", "status": "Resolved"}

@router.post("/complaints/{id}/transition/close")
def transition_to_closed(
    id: int,
    payload: TransitionClose,
    db: Session = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    complaint = db.query(Complaint).filter(Complaint.id == id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
        
    old_status = complaint.status
    if not payload.override and old_status != "Resolved":
        raise HTTPException(
            status_code=400, 
            detail=f"This case must complete the current processing stage before advancing. Expected: Resolved, Current: {old_status}"
        )
        
    complaint.status = "Closed"
    db.commit()
    
    # Save update
    new_update = ComplaintUpdate(
        complaint_id=complaint.id,
        status="Closed",
        previous_status=old_status,
        note=payload.internal_note[:100],
        internal_note=payload.internal_note,
        citizen_update=payload.citizen_update,
        updated_by=current_user.username
    )
    db.add(new_update)
    
    # Log Audit
    action_text = f"Closed the case file."
    if payload.override:
        action_text = f"[OVERRIDE ESCALATION] Bypassed sequence to Close case."
    audit = AuditLog(
        user_id=current_user.id,
        action=action_text,
        complaint_id=complaint.id
    )
    db.add(audit)
    db.commit()
    
    return {"message": "Case file officially Closed.", "status": "Closed"}

@router.get("/ai/model-metrics")
def get_ai_model_metrics(current_user: AdminUser = Depends(get_current_user)):
    """
    Returns full evaluation report, accuracy, precision, recall, confusion matrix, and TF-IDF features.
    """
    from app.ai.evaluate_model import generate_evaluation_metrics
    return generate_evaluation_metrics()

@router.post("/ai/test-inference")
def test_ai_inference(
    payload: dict,
    current_user: AdminUser = Depends(get_current_user)
):
    """
    Live AI Sandbox test endpoint for faculty/guide review demos.
    """
    from app.ai.classifier import ai_service
    text = payload.get("text", "")
    amount = float(payload.get("amount", 0.0)) if payload.get("amount") else None
    return ai_service.analyze_complaint(text, amount_involved=amount)
