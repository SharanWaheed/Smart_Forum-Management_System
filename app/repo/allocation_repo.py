from app import db
from app.models.allocation import ResourceAllocation
from app.models.users_model import User
from app.models.task_model import Task
from app.exceptions import BadRequestException, NotFoundException, DatabaseException

class AllocationRepository:
    @staticmethod
    def allocate_user(user_id, project_id=None, task_id=None, status="Active"):
        """Allocates a user to a task or project, ensuring valid user and role retrieval."""
        
        # Fetch the user by ID
        user = User.query.get(user_id)
        if not user:
            raise NotFoundException("User not found.")

        # Extract role and email from the user record
        role = user.role
        user_email = user.email

        # Create a new allocation record
        allocation = ResourceAllocation(
            user_id=user_id,
            project_id=project_id,
            task_id=task_id,
            role=role,
            status=status
        )

        # Commit the allocation to the database and return result + email
        try:
            db.session.add(allocation)
            db.session.commit()
            return allocation, user_email  # Returning both for BL use
        except Exception as e:
            db.session.rollback()
            raise DatabaseException(f"Database error during allocation: {str(e)}")

    @staticmethod
    def update_allocation(allocation_id, project_id=None, task_id=None, status=None):
        """Updates an existing allocation record based on the provided fields."""
        allocation = ResourceAllocation.query.get(allocation_id)
        if not allocation:
            raise NotFoundException("Allocation not found.")

        if project_id is None and task_id is None and status is None:
            raise BadRequestException("At least one field (project_id, task_id, or status) must be provided for update.")

        if project_id is not None:
            allocation.project_id = project_id

        if task_id is not None:
            task = Task.query.get(task_id)
            if not task:
                raise NotFoundException("Task not found.")
            allocation.task_id = task_id

        if status is not None:
            allocation.status = status

        db.session.commit()
        return allocation

    @staticmethod
    def deallocate_user(allocation_id):
        """Deletes an allocation record."""
        allocation = ResourceAllocation.query.get(allocation_id)
        if not allocation:
            raise NotFoundException("Allocation not found.")

        try:
            db.session.delete(allocation)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise DatabaseException(f"Database error during deletion: {str(e)}")

    @staticmethod
    def get_allocations():
        """Fetches all allocations."""
        try:
            return ResourceAllocation.query.all()
        except Exception as e:
            raise DatabaseException(f"Database error during fetching allocations: {str(e)}")






