import pytest
from src import create_app, db  # updated
from src.api.models import User

############################################################################################
# 如果希望fixture被多个测试文件共享，可以在公共目录下创建一个conftest.py文件，将fixture放在其中。
############################################################################################

@pytest.fixture(scope='module')
def test_app():
    app = create_app()
    app.config.from_object('src.config.TestingConfig')
    with app.app_context():
        print("[fixture] In test_app(), before yield")
        yield app  # testing happens here
        print("[fixture] In test_app(), after yield")


@pytest.fixture(scope='module')
def test_database():
    # Before test, firstly prepare database.
    db.create_all()
    print("[fixture] In test_database(), before yield")
    yield db  # testing happens here
    print("[fixture] In test_database(), after yield")
    db.session.remove()
    # After test, finally close the database. 
    db.drop_all()


@pytest.fixture(scope='function')
def add_user():
    def _add_user(username, email):
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return user
    return _add_user
