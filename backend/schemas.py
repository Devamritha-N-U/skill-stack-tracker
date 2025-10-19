from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# --- Base Schema (Shared attributes for reading and writing) ---
class GoalBase(BaseModel):
    """Base schema containing common fields for creating and reading goals."""
    # Renamed from 'name' to 'skill_name'
    skill_name: str = Field(..., max_length=100) 
    resource_type: str = Field(..., max_length=50, description="e.g., course, video, book")
    platform: str = Field(..., max_length=100, description="e.g., Udemy, YouTube, Coursera")
    # Added target_hours (crucial for progress calculation)
    target_hours: int = Field(..., ge=1, description="Total hours targeted for mastery.")
    difficulty_rating: int = Field(..., ge=1, le=10)
    
# --- Creation Schema (INPUT DATA) ---
class GoalCreate(GoalBase):
    """Schema for creating a new goal (inherits all required fields from GoalBase)."""
    pass

# --- Update Schema (INPUT DATA for PATCH) ---
class GoalUpdate(BaseModel):
    """Schema for updating an existing goal (all fields are optional)."""
    # Renamed from 'name' to 'skill_name'
    skill_name: Optional[str] = Field(None, max_length=100)
    resource_type: Optional[str] = Field(None, max_length=50)
    platform: Optional[str] = Field(None, max_length=100)
    target_hours: Optional[int] = Field(None, ge=1)
    difficulty_rating: Optional[int] = Field(None, ge=1, le=10)
    
    # Fields commonly updated for progress tracking
    status: Optional[str] = Field(None, max_length=50, description="pending, started, in-progress, completed, on-hold")
    hours_spent: Optional[float] = Field(None, ge=0.0) # Changed to float
    notes: Optional[str] = Field(None, max_length=5000)

# --- Read Schema (OUTPUT DATA) ---
class SkillGoal(GoalBase):
    """Schema for reading a goal, includes database-generated fields."""
    id: int
    status: str
    hours_spent: float # Changed to float
    notes: Optional[str] = None
    
    # Timestamps added for completeness
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        # Crucial for SQLAlchemy models to work with Pydantic
        from_attributes = True 
