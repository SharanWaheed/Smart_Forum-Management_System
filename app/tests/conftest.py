import pytest
from app import create_app, db
from app.models.task_model import Task
from datetime import date


@pytest.fixture(scope="session")
def test_app():
    """Creates a Flask test application with context."""
    app = create_app("testing")
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def client(test_app): #oRIGNAL SERVER KO RUN KIYE BAJAIE
    """Provides a test client inside the correct app context."""
    with test_app.test_client() as client:
        with test_app.app_context():
            yield client


@pytest.fixture(scope="function")
def init_database(test_app): #Prevents leftover test data from affecting other tests.
    """Sets up the test database before each test."""
    with test_app.app_context():
        db.session.begin_nested()  # Start a transaction to rollback after test
        yield db
        db.session.rollback()  # Rollback to keep DB clean


@pytest.fixture
def setup_task(init_database): #Allows tests to work with a predefined test task instead of creating new ones each time.
    """Creates a sample task for testing."""
    task = Task(
        title="Test Task",
        description="Task description",
        due_date=date(2025, 12, 31)   
    )
    db.session.add(task)
    db.session.commit()
    yield task
    db.session.delete(task)
    db.session.commit()


@pytest.fixture(scope="function", autouse=True)
def cleanup_db():
    """Ensure DB session is cleaned up after each test."""
    yield
    db.session.rollback()
    db.session.remove()



# conftest.py	Sets up the test environment (app, database, test client)
# Test Database	Created in-memory for testing (db.create_all() in app())
# client	Simulates API requests without running a server
# init_database()	Loads test data before running tests
# Test Cases	Validate API behavior (create, get, update, delete tasks)
# db.drop_all()	Cleans up the database after tests