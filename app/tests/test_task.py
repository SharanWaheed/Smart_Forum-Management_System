import pytest
from app import db
from app.models.task_model import Task
from app.repo.task_repo import TaskRepository
from datetime import date, datetime



def test_create_task(client):
    """Test creating a new task."""
    #Client.post use kr rahe hain postman ki jaaga
    response = client.post(
        "/tasks/create",
        json={
            "title": "New Task",
            "description": "Test Desc",
            "due_date": date(2025, 12, 31).isoformat()  #   Convert to ISO format
        },
    )
    assert response.status_code == 201  # Ensure creation was successful warna AssertionError raise hoga


def test_get_all_tasks():
    """Test retrieving all tasks."""
    tasks = TaskRepository.get_all_tasks()
    assert isinstance(tasks, list)


def test_get_task_by_id(setup_task):
    """Test retrieving a task by ID."""
    task = TaskRepository.get_task_by_id(setup_task.id)
    assert task is not None
    assert task.id == setup_task.id


def test_update_task(setup_task):
    """Test updating a task."""
    updated_task = TaskRepository.update_task(setup_task.id, title="Updated Task")
    assert updated_task is not None
    assert updated_task.title == "Updated Task"


def test_delete_task(setup_task):
    """Test deleting a task."""
    success = TaskRepository.delete_task(setup_task.id)
    assert success is True
    task = TaskRepository.get_task_by_id(setup_task.id)
    assert task is None


def test_assign_task_to_project(setup_task):
    """Test assigning a task to a project."""
    response = TaskRepository.assign_task_to_project(setup_task.id, project_id=1)
    assert "message" in response
    assert response["message"] == "Task assigned successfully" #  Passes if the response has a "message" key.


def test_remove_task_from_project(setup_task):
    """Test removing a task from a project."""
    response = TaskRepository.remove_task_from_project(project_id=1, task_id=setup_task.id)
    assert isinstance(response, bool)  # Expecting a boolean return




 































@pytest.fixture
def setup_task():
    """Fixture to set up a test task."""
    task = TaskRepository.create_task(
        title="Test Task",
        description="This is a test task",
        due_date=date(2025, 12, 31),   
    )
    yield task
    db.session.delete(task)
    db.session.commit()