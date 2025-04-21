import pytest
from sqlalchemy.orm import Session

from app.schemas.publisher import PublisherCreate, PublisherUpdate, PublisherConfigurationUpdate
from app.crud import publisher as publisher_crud
from app.models.publisher import Publisher

class TestPublisherCRUD:
    def test_create_publisher(self, db_session: Session, sample_publisher_data):
        # Create publisher schema
        publisher_in = PublisherCreate(**sample_publisher_data)
        
        # Create publisher in DB
        db_publisher = publisher_crud.create_publisher(db_session, publisher_in)
        
        # Check that publisher was created with correct data
        assert db_publisher.id is not None
        assert db_publisher.id.startswith("pub_")
        assert db_publisher.api_key is not None
        assert db_publisher.api_key.startswith("pk_live_")
        assert db_publisher.company_name == sample_publisher_data["company_name"]
        assert db_publisher.website_url == sample_publisher_data["website_url"]
        assert db_publisher.contact_email == sample_publisher_data["contact_email"]
        assert db_publisher.contact_name == sample_publisher_data["contact_name"]
        assert db_publisher.website_categories == sample_publisher_data["website_categories"]
        assert db_publisher.estimated_monthly_traffic == sample_publisher_data["estimated_monthly_traffic"]
        assert db_publisher.integration_platform == sample_publisher_data["integration_platform"]
        assert db_publisher.preferred_task_types == sample_publisher_data["preferred_task_types"]
        assert db_publisher.is_active is True
        assert db_publisher.created_at is not None
        
        # Check that default configuration was created
        assert "appearance" in db_publisher.configuration
        assert "behavior" in db_publisher.configuration
        assert "task_preferences" in db_publisher.configuration
        assert "rewards" in db_publisher.configuration

    def test_get_publisher(self, db_session: Session, sample_publisher_in_db: Publisher):
        # Get publisher by ID
        db_publisher = publisher_crud.get_publisher(db_session, sample_publisher_in_db.id)
        
        # Check that publisher was retrieved correctly
        assert db_publisher is not None
        assert db_publisher.id == sample_publisher_in_db.id
        assert db_publisher.company_name == sample_publisher_in_db.company_name

    def test_get_publisher_by_email(self, db_session: Session, sample_publisher_in_db: Publisher):
        # Get publisher by email
        db_publisher = publisher_crud.get_publisher_by_email(db_session, sample_publisher_in_db.contact_email)
        
        # Check that publisher was retrieved correctly
        assert db_publisher is not None
        assert db_publisher.id == sample_publisher_in_db.id
        assert db_publisher.contact_email == sample_publisher_in_db.contact_email

    def test_get_publisher_by_api_key(self, db_session: Session, sample_publisher_in_db: Publisher):
        # Get publisher by API key
        db_publisher = publisher_crud.get_publisher_by_api_key(db_session, sample_publisher_in_db.api_key)
        
        # Check that publisher was retrieved correctly
        assert db_publisher is not None
        assert db_publisher.id == sample_publisher_in_db.id
        assert db_publisher.api_key == sample_publisher_in_db.api_key

    def test_get_publishers(self, db_session: Session, sample_publisher_in_db: Publisher):
        # Get all publishers
        publishers = publisher_crud.get_publishers(db_session)
        
        # Check that publishers were retrieved correctly
        assert len(publishers) >= 1
        assert any(p.id == sample_publisher_in_db.id for p in publishers)

    def test_update_publisher(self, db_session: Session, sample_publisher_in_db: Publisher):
        # Create update data
        update_data = PublisherUpdate(
            company_name="Updated Publisher",
            contact_email="updated@example.com",
            estimated_monthly_traffic=200000
        )
        
        # Update publisher
        updated_publisher = publisher_crud.update_publisher(
            db_session, sample_publisher_in_db.id, update_data
        )
        
        # Check that publisher was updated correctly
        assert updated_publisher is not None
        assert updated_publisher.id == sample_publisher_in_db.id
        assert updated_publisher.company_name == "Updated Publisher"
        assert updated_publisher.contact_email == "updated@example.com"
        assert updated_publisher.estimated_monthly_traffic == 200000
        
        # Check that other fields were not updated
        assert updated_publisher.website_url == sample_publisher_in_db.website_url
        assert updated_publisher.contact_name == sample_publisher_in_db.contact_name

    def test_update_publisher_not_found(self, db_session: Session):
        # Create update data
        update_data = PublisherUpdate(company_name="Updated Publisher")
        
        # Try to update non-existent publisher
        updated_publisher = publisher_crud.update_publisher(
            db_session, "non_existent_id", update_data
        )
        
        # Check that no publisher was updated
        assert updated_publisher is None

    def test_update_publisher_configuration(self, db_session: Session, sample_publisher_in_db: Publisher):
        # Create configuration update data
        config_update = PublisherConfigurationUpdate(
            appearance={
                "theme": "dark",
                "primary_color": "#FF5733"
            },
            behavior={
                "task_display_frequency": 600,
                "max_tasks_per_session": 3
            }
        )
        
        # Update publisher configuration
        updated_publisher = publisher_crud.update_publisher_configuration(
            db_session, sample_publisher_in_db.id, config_update
        )
        
        # Check that configuration was updated correctly
        assert updated_publisher is not None
        assert updated_publisher.configuration["appearance"]["theme"] == "dark"
        assert updated_publisher.configuration["appearance"]["primary_color"] == "#FF5733"
        assert updated_publisher.configuration["behavior"]["task_display_frequency"] == 600
        assert updated_publisher.configuration["behavior"]["max_tasks_per_session"] == 3
        
        # Check that other configuration sections were preserved
        assert "task_preferences" in updated_publisher.configuration
        assert "rewards" in updated_publisher.configuration

    def test_update_publisher_configuration_not_found(self, db_session: Session):
        # Create configuration update data
        config_update = PublisherConfigurationUpdate(
            appearance={"theme": "dark"}
        )
        
        # Try to update configuration of non-existent publisher
        updated_publisher = publisher_crud.update_publisher_configuration(
            db_session, "non_existent_id", config_update
        )
        
        # Check that no publisher was updated
        assert updated_publisher is None

    def test_regenerate_api_key(self, db_session: Session, sample_publisher_in_db: Publisher):
        # Store original API key
        original_api_key = sample_publisher_in_db.api_key
        
        # Regenerate API key
        new_api_key = publisher_crud.regenerate_api_key(db_session, sample_publisher_in_db.id)
        
        # Check that API key was regenerated
        assert new_api_key is not None
        assert new_api_key != original_api_key
        assert new_api_key.startswith("pk_live_")
        
        # Check that publisher in DB has new API key
        updated_publisher = publisher_crud.get_publisher(db_session, sample_publisher_in_db.id)
        assert updated_publisher.api_key == new_api_key

    def test_regenerate_api_key_not_found(self, db_session: Session):
        # Try to regenerate API key for non-existent publisher
        new_api_key = publisher_crud.regenerate_api_key(db_session, "non_existent_id")
        
        # Check that no API key was regenerated
        assert new_api_key is None
