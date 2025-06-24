import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from main import app
from db.models import User, Track, Playlist, Base
from db.session import get_db

# Use SQLite in-memory database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def engine():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    # Create all tables before running tests
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # Drop all tables after tests
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    SessionLocal = sessionmaker(bind=connection)
    session = SessionLocal()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def test_db(db_session):
    yield db_session

# ...existing code...

@pytest.fixture
def auth_headers(client, test_db):
    # Create test user
    resp = client.post("/auth/register", json={
        "username": "trackuser",
        "email": "track@example.com",
        "first_name": "Track",
        "last_name": "User",
        "password": "Password123"
    })
    assert resp.status_code == 200
    
    # Login and get token
    login = client.post("/auth/login", data={
        "username": "track@example.com",
        "password": "Password123"
    })
    assert login.status_code == 200
    token = login.json()["access_token"]
    
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def create_test_playlist(client, auth_headers):
    def _create_playlist(name="Test Playlist", description="Test playlist description"):
        playlist_data = {
            "name": name,
            "description": description,
            "tracks": []
        }
        resp = client.post("/playlist/", json=playlist_data, headers=auth_headers)
        assert resp.status_code == 200
        return resp.json()
    return _create_playlist

@pytest.fixture
def create_test_track(client, auth_headers):
    def _create_track(playlist_id, name="Test Track", artist="Test Artist"):
        track_data = {
            "name": name,
            "artist": artist,
            "url": "http://example.com/track",
            "playlist_id": playlist_id
        }
        resp = client.post(
            f"/track/{playlist_id}/tracks",
            json=track_data,
            headers=auth_headers
        )
        assert resp.status_code == 200
        return resp.json()
    return _create_track