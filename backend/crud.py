# crud.py

from sqlalchemy.orm import Session
from typing import List, Dict, Any
from sqlalchemy import func
from datetime import datetime, timedelta

# Import models and schemas from the local package
from . import models, schemas

# --- CRUD Functions for Goals ---

def create_goal(db: Session, goal: schemas.GoalCreate) -> models.Goal:
    """Creates a new Goal object in the database."""
    # Convert Pydantic model to SQLAlchemy model
    db_goal = models.Goal(**goal.dict(), created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

def get_goals(db: Session, skip: int = 0, limit: int = 100) -> List[models.Goal]:
    """Retrieves a list of all goals."""
    return db.query(models.Goal).offset(skip).limit(limit).all()

def get_goal(db: Session, goal_id: int) -> models.Goal | None:
    """Retrieves a single goal by its ID."""
    return db.query(models.Goal).filter(models.Goal.id == goal_id).first()

def update_goal(db: Session, goal_id: int, goal: schemas.GoalUpdate) -> models.Goal | None:
    """Updates an existing goal's details."""
    db_goal = db.query(models.Goal).filter(models.Goal.id == goal_id).first()
    if db_goal:
        # Update attributes from the Pydantic model
        update_data = goal.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_goal, key, value)
        
        # Manually update the timestamp
        db_goal.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(db_goal)
    return db_goal

def delete_goal(db: Session, goal_id: int) -> bool:
    """Deletes a goal by its ID."""
    db_goal = db.query(models.Goal).filter(models.Goal.id == goal_id).first()
    if db_goal:
        db.delete(db_goal)
        db.commit()
        return True
    return False

# --- CRUD Functions for Analytics ---

def get_analytics_summary(db: Session) -> Dict[str, Any]:
    """
    Calculates key metrics and breakdown data for the analytics dashboard.
    This function consolidates all data for the /api/dashboard/analytics endpoint.
    """
    
    # 1. Total Goals and Completed Goals
    total_goals = db.query(models.Goal).count()
    completed_goals = db.query(models.Goal).filter(models.Goal.status == "Completed").count()
    
    # 2. Total Hours Spent
    # Use scalar() to get a single result (the sum)
    total_hours = db.query(func.sum(models.Goal.hours_spent)).scalar() or 0
    
    # 3. Status Breakdown
    status_breakdown = db.query(
        models.Goal.status, 
        func.count()
    ).group_by(models.Goal.status).all()
    
    # 4. Resource Type Breakdown
    resource_breakdown = db.query(
        models.Goal.resource_type, 
        func.count()
    ).group_by(models.Goal.resource_type).all()
    
    # 5. Hours by Skill Name (NEW ADDITION for a primary breakdown chart)
    hours_by_skill = db.query(
        models.Goal.skill_name, 
        func.sum(models.Goal.hours_spent)
    ).group_by(models.Goal.skill_name).all()
    
    # Format the skill hours data
    formatted_skill_hours = [
        {"skill": skill_name, "hours": float(hours) if hours is not None else 0.0}
        for skill_name, hours in hours_by_skill
    ]

    # 6. Hours by Month (Mock data structure for the chart)
    # Aggregates hours spent based on the goal's creation month (simplified).
    one_year_ago = datetime.utcnow() - timedelta(days=365)
    
    hours_by_month_data = db.query(
        func.strftime('%Y-%m', models.Goal.created_at).label('month_year'),
        func.sum(models.Goal.hours_spent).label('total_hours')
    ).filter(
        models.Goal.created_at >= one_year_ago,
        models.Goal.hours_spent > 0
    ).group_by(
        'month_year'
    ).order_by(
        'month_year'
    ).all()
    
    # Format the monthly hours data
    formatted_monthly_data = []
    for month_year, total_hours in hours_by_month_data:
        month_name = datetime.strptime(month_year, '%Y-%m').strftime('%b %Y')
        formatted_monthly_data.append({
            "month": month_name, 
            "total_hours": total_hours
        })
        
    if not formatted_monthly_data:
        formatted_monthly_data.append({"month": datetime.utcnow().strftime('%b %Y'), "total_hours": 0})


    return {
        "total_goals": total_goals,
        "completed_goals": completed_goals,
        "total_hours": total_hours,
        "goal_status_breakdown": {status: count for status, count in status_breakdown},
        "resource_type_breakdown": {resource: count for resource, count in resource_breakdown},
        "skill_hours_breakdown": formatted_skill_hours,  # <-- NEW data for frontend
        "hours_by_month_data": formatted_monthly_data
    }