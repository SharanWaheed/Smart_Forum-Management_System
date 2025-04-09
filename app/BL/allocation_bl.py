from app.repo.allocation_repo import AllocationRepository
from app.exceptions import BadRequestException, NotFoundException, DatabaseException
from app.schema.allocation_schema import AllocationSchema
from app.utils.mail_utils import send_email  

class AllocationBL:
    @staticmethod
    def allocate_user(user_id=None, task_id=None, project_id=None, status="Active"):
        if user_id is None:
            return {"error": "Missing required field: user_id"}, 400
        if task_id is None and project_id is None:
            return {"error": "Either task_id or project_id must be provided"}, 400

        try:
            # Get allocation and user email from repository
            allocation, user_email = AllocationRepository.allocate_user(
                user_id=user_id,
                task_id=task_id,
                project_id=project_id,
                status=status
            )

            # Validate the email
            if not user_email or "@" not in user_email:
                return {"error": "Invalid or missing email address for the user"}, 400

            #  Prepare and send email
            subject = "Task Allocation Notification"
            body = f"Dear User as you know your id is  {user_id},\n\nYou have been successfully allocated to a new task/project. Kindly open Workbench to check."
            send_email(subject, user_email, body)
        
            return {
                "message": "User allocated successfully!",
                "allocation": {
                    "user_id": allocation.user_id,
                    "task_id": allocation.task_id,
                    "project_id": allocation.project_id,
                    "status": allocation.status
                }
            }, 201

        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500

    @staticmethod
    def update_allocation(data):
        """Handles allocation updates while ensuring correct field validation."""
        try:
            allocation_id = data.get("allocation_id")
            project_id = data.get("project_id")
            task_id = data.get("task_id")
            status = data.get("status")

            if not allocation_id:
                raise BadRequestException("Missing required field: allocation_id.")

            updated_allocation = AllocationRepository.update_allocation(
                allocation_id, project_id, task_id, status
            )

            return {
                "message": "Allocation updated successfully",
                "allocation": AllocationSchema().dump(updated_allocation)
            }, 200

        except NotFoundException as e:
            return {"error": str(e)}, 404
        except BadRequestException as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500

    @staticmethod
    def deallocate_user(allocation_id: int):
        """Handles deallocating a user while ensuring proper error handling."""
        try:
            AllocationRepository.deallocate_user(allocation_id)
            return {"message": "User deallocated successfully!"}, 200
        except NotFoundException as e:
            return {"error": str(e)}, 404
        except DatabaseException as e:
            return {"error": str(e)}, 500
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500

    @staticmethod
    def get_allocations():
        """Fetches all allocations with proper error handling."""
        try:
            allocations = AllocationRepository.get_allocations()
            return [AllocationSchema().dump(allocation) for allocation in allocations], 200
        except DatabaseException as e:
            return {"error": str(e)}, 500
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500
