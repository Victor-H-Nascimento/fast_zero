import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import User, table_registry
from fast_zero.security import get_password_hash


@pytest.fixture()  # noqa: PT001
def client(session: Session):
    def get_session_overrides():
        return session

    with TestClient(app) as client:  # Arrange (Organização)
        app.dependency_overrides[get_session] = get_session_overrides
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()  # noqa: PT001
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture()  # noqa: PT001
def user(session: Session):
    password = 'testtest'
    user = User(
        username='Teste',
        email='teste@test.com',
        password=get_password_hash(password),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # user.clean_password = password  # hack - Monkey Patch

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        'auth/token', data={'username': user.email, 'password': user.password}
    )
    return response.json()['access_token']
