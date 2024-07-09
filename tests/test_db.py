from sqlalchemy import select

from fast_zero.models import User


def teste_create_user(session):
    user = User(
        username='victor',
        email='vic@tor.com.br',
        password='victor123',
    )

    session.add(user)
    session.commit()
    # session.refresh(user)

    result: User = session.scalar(
        select(User).where(User.email == 'vic@tor.com.br')
    )

    assert result.username == 'victor'
    assert result.id == 1
