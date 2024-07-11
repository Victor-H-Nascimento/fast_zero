from http import HTTPStatus

from fast_zero.schemas import UserPublic, UserSchema


def test_read_root_should_return_ok_and_hello_world(client):
    response = client.get('/')  # Act (Ação)

    assert response.status_code == HTTPStatus.OK  # Assert (Afirmação)
    assert response.json() == {'message': 'Olár mundo!'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'string',
            'email': 'user@example.com',
            'password': 'string',
        },
    )  # Act (Ação)

    assert response.status_code == HTTPStatus.CREATED  # Assert (Afirmação)
    assert response.json() == {
        'id': 1,
        'username': 'string',
        'email': 'user@example.com',
    }


def test_create_user_with_used_username(client, user):
    user_schema = UserSchema.model_validate(user).model_dump()

    response = client.post(
        '/users/',
        json=user_schema,
    )  # Act (Ação)

    assert response.status_code == HTTPStatus.BAD_REQUEST  # Assert (Afirmação)
    assert response.json() == {
        'detail': 'Username já existe',
    }


def test_create_user_with_used_email(client, user):
    user_schema = UserSchema.model_validate(user).model_dump()
    user_schema['username'] = 'nome_diferente'

    response = client.post(
        '/users/',
        json=user_schema,
    )  # Act (Ação)
    assert response.status_code == HTTPStatus.BAD_REQUEST  # Assert (Afirmação)
    assert response.json() == {
        'detail': 'Email já existe',
    }


def test_read_users(client):
    response = client.get(
        '/users/',
    )  # Act (Ação)

    assert response.status_code == HTTPStatus.OK  # Assert (Afirmação)
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')  # Act (Ação)
    assert response.json() == {'users': [user_schema]}


def test_read_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/1')  # Act (Ação)
    assert response.status_code == HTTPStatus.OK  # Assert (Afirmação)
    assert response.json() == user_schema


def test_read_user_not_found_user(client):
    response = client.get('/users/1')  # Act (Ação)
    assert response.status_code == HTTPStatus.NOT_FOUND  # Assert (Afirmação)


def test_update_user(client, user):
    user_schema = UserSchema.model_validate(user).model_dump()
    user_schema['username'] = 'nome_diferente'

    user_response = UserPublic.model_validate(user).model_dump()
    user_response['username'] = 'nome_diferente'
    response = client.put(
        '/users/1',
        json=user_schema,
    )  # Act (Ação)

    assert response.status_code == HTTPStatus.OK  # Assert (Afirmação)
    assert response.json() == user_response


def test_update_not_found_user(client, user):
    user_schema = UserSchema.model_validate(user).model_dump()
    response = client.put(
        '/users/-1',
        json=user_schema,
    )  # Act (Ação)

    assert response.status_code == HTTPStatus.NOT_FOUND  # Assert (Afirmação)


def test_delete_user(client, user):
    response = client.delete(
        '/users/1',
    )  # Act (Ação)

    assert response.status_code == HTTPStatus.OK  # Assert (Afirmação)
    assert response.json() == {'message': 'User with id 1 deleted!'}


def test_delete_not_found_user(client):
    response = client.delete(
        '/users/-1',
    )  # Act (Ação)

    assert response.status_code == HTTPStatus.NOT_FOUND  # Assert (Afirmação)
