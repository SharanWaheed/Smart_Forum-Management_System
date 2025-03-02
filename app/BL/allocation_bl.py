from datetime import datetime
from flask import current_app

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from app.models.allocation import ResourceAllocation

class AllocationBL:
    @staticmethod
    def allocate_user(project_id=None, task_id=None, user_id=None, status="Active"):
        db = current_app.extensions['sqlalchemy'].db  
        allocation = ResourceAllocation(
            project_id=project_id,
            task_id=task_id,
            user_id=user_id,
            status=status,
            allocated_at=datetime.utcnow()
        )
        db.session.add(allocation)
        db.session.commit()

        return {  # ✅ Return a dictionary instead of a model object
            "id": allocation.id,
            "project_id": allocation.project_id,
            "task_id": allocation.task_id,
            "user_id": allocation.user_id,
            "status": allocation.status,
            "allocated_at": allocation.allocated_at
        }, 201
    
    @staticmethod
    def update_allocation(allocation_id, status=None):
        allocation = ResourceAllocation.query.get(allocation_id)
        
        if not allocation:
            return {"error": "Allocation not found"}, 404
        
        if status:
            allocation.status = status
            db.session.commit()
        
        return {"message": "Allocation updated successfully"}, 200
    
    @staticmethod
    def deallocate_user(allocation_id):
        allocation = ResourceAllocation.query.get(allocation_id)
        
        if not allocation:
            return {"error": "Allocation not found"}, 404
        
        db.session.delete(allocation)
        db.session.commit()
        
        return {"message": "User deallocated successfully"}, 200
    
    @staticmethod
    def get_allocations():
        allocations = ResourceAllocation.query.all()
        
        return [{
            "id": alloc.id,
            "project_id": alloc.project_id,
            "task_id": alloc.task_id,
            "user_id": alloc.user_id,
            "status": alloc.status,
            "assigned_at": alloc.assigned_at
        } for alloc in allocations]
