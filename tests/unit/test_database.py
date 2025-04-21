import pytest
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

from app.core.database import get_db, Base, engine, SessionLocal

class TestDatabase:
    def test_engine_exists(self):
        """Test that the engine is created."""
        assert engine is not None
        assert isinstance(engine, Engine)

    def test_session_local(self):
        """Test that SessionLocal can create a session."""
        session = SessionLocal()
        try:
            assert session is not None
            assert isinstance(session, Session)
        finally:
            session.close()

    def test_get_db(self):
        """Test that get_db yields a session."""
        # get_db is a generator, so we need to use next() to get the session
        db_generator = get_db()
        db = next(db_generator)
        
        try:
            assert db is not None
            assert isinstance(db, Session)
        finally:
            # We need to close the generator by sending a value
            try:
                db_generator.send(None)
            except StopIteration:
                pass

    def test_base_exists(self):
        """Test that Base exists."""
        assert Base is not None
        assert hasattr(Base, 'metadata')
        assert hasattr(Base, '__tablename__')
