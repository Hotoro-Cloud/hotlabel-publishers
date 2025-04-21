import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app

# Create in-memory SQLite database for testing
@pytest.fixture(scope="session")
def engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(engine):
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

@pytest.fixture(scope="function")
def client(db_session):
    # Override the get_db dependency
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

@pytest.fixture
def sample_publisher_data():
    return {
        "company_name": "Test Publisher",
        "website_url": "https://testpublisher.com",
        "contact_email": "contact@testpublisher.com",
        "contact_name": "John Doe",
        "website_categories": ["news", "technology"],
        "estimated_monthly_traffic": 100000,
        "integration_platform": "wordpress",
        "preferred_task_types": ["survey", "feedback"]
    }

@pytest.fixture
def sample_publisher_in_db(db_session, sample_publisher_data):
    from app.schemas.publisher import PublisherCreate
    from app.crud.publisher import create_publisher
    
    publisher_in = PublisherCreate(**sample_publisher_data)
    db_publisher = create_publisher(db_session, publisher_in)
    return db_publisher
