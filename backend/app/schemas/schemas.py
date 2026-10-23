from pydantic import BaseModel, Field, model_validator
from datetime import datetime, date
from typing import List, Optional

# Auth Schemas
class UserLogin(BaseModel):
    username: str
    password: str

class UserRegister(BaseModel):
    full_name: str
    email: str
    username: str
    department: str
    role: str = "Officer"
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    full_name: Optional[str]
    email: Optional[str]
    department: Optional[str]
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

class CitizenRegister(BaseModel):
    username: str
    email: str
    password: str

class CitizenResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    username: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

# Evidence Schemas
class EvidenceResponse(BaseModel):
    id: int
    file_name: str
    file_type: str
    uploaded_at: datetime

    class Config:
        from_attributes = True

# AI Prediction Schemas
class AIPredictionResponse(BaseModel):
    predicted_category: str
    category_confidence: float
    predicted_priority: str
    priority_confidence: float
    recommended_department: str
    department_confidence: float
    duplicate_score: float
    suspicious_flag: bool

    class Config:
        from_attributes = True

# Assignment Schemas
class AssignmentCreate(BaseModel):
    assigned_department: str
    assigned_officer: Optional[str] = None

class AssignmentResponse(BaseModel):
    id: int
    assigned_department: str
    assigned_officer: Optional[str]
    assigned_at: datetime

    class Config:
        from_attributes = True

# Complaint Update Schemas
class ComplaintUpdateCreate(BaseModel):
    status: str
    note: str
    internal_note: Optional[str] = None
    citizen_update: Optional[str] = None

class ComplaintUpdateResponse(BaseModel):
    id: int
    status: str
    previous_status: Optional[str]
    note: str
    internal_note: Optional[str]
    citizen_update: Optional[str]
    updated_by: str
    created_at: datetime

    class Config:
        from_attributes = True

class ComplaintUpdatePublicResponse(BaseModel):
    id: int
    status: str
    note: str # Mapped from citizen_update for citizen frontend compatibility
    created_at: datetime

    class Config:
        from_attributes = True

    @model_validator(mode="before")
    @classmethod
    def map_citizen_update_to_note(cls, data):
        if hasattr(data, "citizen_update"):
            return {
                "id": data.id,
                "status": data.status,
                "note": data.citizen_update or data.note or "",
                "created_at": data.created_at
            }
        elif isinstance(data, dict):
            return {
                "id": data.get("id"),
                "status": data.get("status"),
                "note": data.get("citizen_update") or data.get("note") or "",
                "created_at": data.get("created_at")
            }
        return data

class CaseActionResponse(BaseModel):
    id: int
    action_type: str
    action_description: str
    suggested_by_ai: bool
    approved_by: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# Complaint Create (Citizen Input)
class ComplaintCreate(BaseModel):
    category: Optional[str] = None
    department: Optional[str] = None
    description: str
    location: Optional[str] = None
    incident_date: Optional[date] = None
    amount_involved: Optional[float] = None

# Public Complaint Response (Citizen View)
class ComplaintPublicResponse(BaseModel):
    tracking_id: str
    category: Optional[str]
    department: Optional[str]
    location: Optional[str]
    incident_date: Optional[date]
    amount_involved: Optional[float]
    status: str
    created_at: datetime
    updates: List[ComplaintUpdatePublicResponse] = []

    class Config:
        from_attributes = True

# Admin Complaint Response (Full View)
class ComplaintAdminResponse(BaseModel):
    id: int
    tracking_id: str
    description: str
    category: Optional[str]
    department: Optional[str]
    location: Optional[str]
    incident_date: Optional[date]
    amount_involved: Optional[float]
    priority: str
    status: str
    next_status: Optional[str]
    verification_code: Optional[str]
    created_at: datetime
    updated_at: datetime
    evidence: List[EvidenceResponse] = []
    ai_prediction: Optional[AIPredictionResponse] = None
    updates: List[ComplaintUpdateResponse] = []
    assignments: List[AssignmentResponse] = []
    case_actions: List[CaseActionResponse] = []

    class Config:
        from_attributes = True

# Dashboard Stats Schemas
class DashboardStats(BaseModel):
    total_complaints: int
    pending_complaints: int
    under_investigation: int
    resolved_complaints: int
    high_priority: int
    critical_priority: int
    duplicate_flags: int
    suspicious_flags: int

# Analytics Schemas
class ChartDataPoint(BaseModel):
    name: str
    value: int

class TrendDataPoint(BaseModel):
    date: str
    count: int

class AnalyticsResponse(BaseModel):
    by_department: List[ChartDataPoint]
    by_category: List[ChartDataPoint]
    by_priority: List[ChartDataPoint]
    monthly_trends: List[TrendDataPoint]
    resolution_rate: float


class AdvanceRequest(BaseModel):
    note: str

class ConfirmAdvance(BaseModel):
    code: str
    note: str

class TransitionUnderReview(BaseModel):
    priority: Optional[str] = None
    category: Optional[str] = None
    internal_note: str
    citizen_update: str
    override: Optional[bool] = False

class TransitionAssign(BaseModel):
    department: str
    internal_note: str
    citizen_update: str
    approved_actions: List[str] = []
    override: Optional[bool] = False

class TransitionInvestigate(BaseModel):
    officer: str
    internal_note: str
    citizen_update: str
    override: Optional[bool] = False

class TransitionResolve(BaseModel):
    resolution_type: str
    resolution_summary: str
    internal_note: str
    citizen_update: str
    override: Optional[bool] = False

class TransitionClose(BaseModel):
    internal_note: str
    citizen_update: str
    override: Optional[bool] = False

class AddCaseAction(BaseModel):
    action_type: str
    action_description: str
