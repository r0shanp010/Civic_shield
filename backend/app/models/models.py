from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    tracking_id = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=True) # Input by user (optional/rough)
    department = Column(String(100), nullable=True) # Input by user
    location = Column(String(255), nullable=True)
    incident_date = Column(Date, nullable=True)
    amount_involved = Column(Float, nullable=True)
    priority = Column(String(50), default="Medium")
    status = Column(String(50), default="Pending") # Pending, Under Review, Assigned, Investigating, Resolved, Closed
    next_status = Column(String(50), nullable=True)
    verification_code = Column(String(10), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="complaints")
    evidence = relationship("Evidence", back_populates="complaint", cascade="all, delete-orphan")
    ai_prediction = relationship("AIPrediction", back_populates="complaint", uselist=False, cascade="all, delete-orphan")
    updates = relationship("ComplaintUpdate", back_populates="complaint", cascade="all, delete-orphan")
    assignments = relationship("Assignment", back_populates="complaint", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="complaint", cascade="all, delete-orphan")
    case_actions = relationship("CaseAction", back_populates="complaint", cascade="all, delete-orphan")


class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id", ondelete="CASCADE"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(100), nullable=False)
    file_path = Column(String(500), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    complaint = relationship("Complaint", back_populates="evidence")


class AIPrediction(Base):
    __tablename__ = "ai_predictions"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id", ondelete="CASCADE"), nullable=False)
    predicted_category = Column(String(100), nullable=False)
    category_confidence = Column(Float, nullable=False)
    predicted_priority = Column(String(50), nullable=False)
    priority_confidence = Column(Float, nullable=False)
    recommended_department = Column(String(100), nullable=False)
    department_confidence = Column(Float, nullable=False)
    duplicate_score = Column(Float, default=0.0) # Cosine similarity percentage (0-100)
    suspicious_flag = Column(Boolean, default=False) # True if manual check required
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    complaint = relationship("Complaint", back_populates="ai_prediction")


class ComplaintUpdate(Base):
    __tablename__ = "complaint_updates"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), nullable=False)
    previous_status = Column(String(50), nullable=True)
    note = Column(Text, nullable=False) # fallback/summary
    internal_note = Column(Text, nullable=True)
    citizen_update = Column(Text, nullable=True)
    updated_by = Column(String(100), nullable=False) # Admin username or System
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    complaint = relationship("Complaint", back_populates="updates")


class CaseAction(Base):
    __tablename__ = "case_actions"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id", ondelete="CASCADE"), nullable=False)
    action_type = Column(String(100), nullable=False) # e.g. "Review Transaction Records"
    action_description = Column(String(255), nullable=False)
    suggested_by_ai = Column(Boolean, default=False)
    approved_by = Column(String(100), nullable=True) # officer username if approved
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    complaint = relationship("Complaint", back_populates="case_actions")


class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(150), nullable=True)
    email = Column(String(150), unique=True, index=True, nullable=True)
    department = Column(String(100), nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="Officer") # Admin, Officer
    created_at = Column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    complaints = relationship("Complaint", back_populates="user")


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id", ondelete="CASCADE"), nullable=False)
    assigned_department = Column(String(100), nullable=False)
    assigned_officer = Column(String(100), nullable=True)
    assigned_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    complaint = relationship("Complaint", back_populates="assignments")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("admin_users.id", ondelete="SET NULL"), nullable=True)
    action = Column(String(255), nullable=False)
    complaint_id = Column(Integer, ForeignKey("complaints.id", ondelete="CASCADE"), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationship
    complaint = relationship("Complaint", back_populates="audit_logs")
