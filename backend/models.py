from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base # Import Base from the local database module

class Goal(Base):
    __tablename__ = "goals"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Core Goal Fields (Aligned with frontend/API schemas)
    skill_name = Column(String, index=True, nullable=False) # Changed from 'name' to 'skill_name'
    target_hours = Column(Integer, nullable=False)          # Re-added: Crucial for progress tracking

    # Resource Details
    resource_type = Column(String, default="Course")        # e.g., Course, Video, Book
    platform = Column(String, nullable=False)               # e.g., Udemy, YouTube
    difficulty_rating = Column(Integer, default=3)          # Using a 1-5 scale for consistency with frontend

    # Progress and Tracking fields
    status = Column(String, default="Started")              # Aligned with frontend options
    hours_spent = Column(Float, default=0.0)                # Using Float for potential half-hours
    notes = Column(String, default="")
    
    # Timestamps (Using Python datetime for SQLite compatibility)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Goal(skill_name='{self.skill_name}', status='{self.status}')>"
