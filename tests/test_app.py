from http import HTTPStatus


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


def test_read_users(client):
    response = client.get(
        '/users/',
    )  # Act (Ação)

    assert response.status_code == HTTPStatus.OK  # Assert (Afirmação)
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'string',
                'email': 'user@example.com',
            }
        ]
    }


def test_read_user(client):
    response = client.get(
        '/users/1',
    )  # Act (Ação)

    assert response.status_code == HTTPStatus.OK  # Assert (Afirmação)
    assert response.json() == {
        'username': 'string',
        'email': 'user@example.com',
        'id': 1,
    }

def test_read_user_not_found_user(client):
    response = client.get(
        '/users/-1',
    )  # Act (Ação)

    assert response.status_code == HTTPStatus.NOT_FOUND  # Assert (Afirmação)


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'victor',
            'email': 'user@example.com',
            'password': 'string',
            'id': 1,
        },
    )  # Act (Ação)

    assert response.status_code == HTTPStatus.OK  # Assert (Afirmação)
    assert response.json() == {
        'id': 1,
        'username': 'victor',
        'email': 'user@example.com',
    }


def test_update_not_found_user(client):
    response = client.put(
        '/users/-1',
        json={
            'username': 'victor',
            'email': 'user@example.com',
            'password': 'string',
            'id': -1,
        },
    )  # Act (Ação)

    assert response.status_code == HTTPStatus.NOT_FOUND  # Assert (Afirmação)


def test_delete_user(client):
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
