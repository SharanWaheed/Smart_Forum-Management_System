from sqlalchemy.orm import Session
from app.models.allocation import ResourceAllocation
from app.models.users_model import User
from app.models.project_model import Project
from app.models.task_model import Task

def allocate_user(db: Session, user_id: int, project_id: int = None, task_id: int = None, status: str = "Active"):
    """Assign a user to a project or task."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None  # User not found
    
    allocation = ResourceAllocation(user_id=user_id, project_id=project_id, task_id=task_id, role=user.role, status=status)
    db.add(allocation)
    db.commit()
    db.refresh(allocation)
    return allocation

def update_allocation(db: Session, allocation_id: int, status: str = None):
    """Update an existing allocation's status."""
    allocation = db.query(ResourceAllocation).filter(ResourceAllocation.id == allocation_id).first()
    if not allocation:
        return None  # Allocation not found
    
    if status:
        allocation.status = status
    
    db.commit()
    db.refresh(allocation)
    return allocation

def deallocate_user(db: Session, allocation_id: int):
    """Remove a user allocation."""
    allocation = db.query(ResourceAllocation).filter(ResourceAllocation.id == allocation_id).first()
    if not allocation:
        return None  # Allocation not found
    
    db.delete(allocation)
    db.commit()
    return True

def get_allocations(db: Session, project_id: int = None, task_id: int = None):
    """Fetch allocations, optionally filtering by project or task."""
    query = db.query(ResourceAllocation).join(User).with_entities(
        ResourceAllocation.id, ResourceAllocation.project_id, ResourceAllocation.task_id,
        ResourceAllocation.user_id, User.role, ResourceAllocation.status, ResourceAllocation.assigned_at
    )
    
    if project_id:
        query = query.filter(ResourceAllocation.project_id == project_id)
    if task_id:
        query = query.filter(ResourceAllocation.task_id == task_id)
    
    return query.all()
