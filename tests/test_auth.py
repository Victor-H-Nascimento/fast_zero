from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        'auth/token',
        data={'username': user.email, 'password': user.password},
    )  # Act (Ação)

    token = response.json()

    assert response.status_code == HTTPStatus.OK  # Assert (Afirmação)
    assert token['token_type'] == 'Bearer'  # Assert (Afirmação)
    assert 'access_token' in token  # Assert (Afirmação)
