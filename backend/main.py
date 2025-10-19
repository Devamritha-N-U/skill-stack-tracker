# main.py

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict, Any # Dict and Any are needed for the analytics endpoint

from . import crud
from . import models, schemas # Ensure schemas is imported
from .database import SessionLocal, engine

# --- Database Setup ---
# Create all tables defined in models.py (if they don't already exist)
models.Base.metadata.create_all(bind=engine)

# Dependency to get a new DB session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Application Instance ---
app = FastAPI(
    title="Skill Tracker API",
    description="API for managing personal learning goals and progress.",
    version="1.0.0"
)

# --- CORS Configuration ---
# Ensure the React frontend can talk to the FastAPI backend
origins = [
    "http://localhost:3000",  # Default React Dev Server
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routes ---

# Root check
@app.get("/")
def read_root():
    return {"message": "Welcome to the Skill Tracker API"}

# GET: Read All Goals
@app.get("/goals/", response_model=List[schemas.SkillGoal])
def read_goals(db: Session = Depends(get_db)):
    """Retrieve all existing skill goals."""
    goals = crud.get_goals(db)
    return goals

# POST: Create Skill Goal
@app.post("/goals/", response_model=schemas.SkillGoal, status_code=status.HTTP_201_CREATED)
def create_goal(goal: schemas.GoalCreate, db: Session = Depends(get_db)):
    """Create a new skill goal."""
    return crud.create_goal(db=db, goal=goal)

# PATCH: Update Skill Goal (Progress Tracking)
@app.patch("/goals/{goal_id}", response_model=schemas.SkillGoal)
def update_goal(goal_id: int, goal_update: schemas.GoalUpdate, db: Session = Depends(get_db)):
    """Update progress, status, hours_spent, or notes for a specific goal."""
    db_goal = crud.update_goal(db, goal_id=goal_id, goal=goal_update)
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    return db_goal

# GET: Read Single Goal
@app.get("/goals/{goal_id}", response_model=schemas.SkillGoal)
def read_single_goal(goal_id: int, db: Session = Depends(get_db)):
    """Retrieve a single skill goal by its ID."""
    db_goal = crud.get_goal(db, goal_id=goal_id)
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    return db_goal

# *** DASHBOARD ANALYTICS ENDPOINT ***
# This endpoint retrieves ALL data required for your dashboard (tiles and charts).
@app.get("/analytics/summary", response_model=Dict[str, Any])
def get_analytics_summary(db: Session = Depends(get_db)):
    """Retrieve overall analytics summary and breakdown data."""
    # This calls the single, fully implemented CRUD function from crud.py
    return crud.get_analytics_summary(db)

# DELETE: Delete Skill Goal (Bonus feature for complete CRUD)
@app.delete("/goals/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(goal_id: int, db: Session = Depends(get_db)):
    """Delete a skill goal by its ID."""
    success = crud.delete_goal(db, goal_id=goal_id)
    if not success:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    # Return nothing for 204 No Content status
    return