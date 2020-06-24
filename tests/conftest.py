from datetime import datetime
import pytest
from flaskblog import create_test_app, db, bcrypt
from flaskblog.models import User, Post


@pytest.fixture
def app_with_test_data_in_db():
    app = create_test_app()
    with app.app_context():
        db.create_all()
        test_user_1 = User(username="testUser1", email="testUser1@gmail.com",
                           password=bcrypt.generate_password_hash("Password1!")
                           .decode('utf-8'),
                           is_activated=True)
        test_post_1 = Post(title="test_title1",
                           date_posted=datetime(2013, 10, 12, 8, 25, 43),
                           content="test_content1", author=test_user_1)
        test_user_2 = User(username="testUser2", email="testUser2@gmail.com",
                           password=bcrypt.generate_password_hash("Password1!")
                           .decode('utf-8'),
                           is_activated=True)
        test_post_2 = Post(title="test_title2",
                           date_posted=datetime(2013, 10, 12, 8, 25, 43),
                           content="test_content2", author=test_user_2)
        db.session.add(test_user_1)
        db.session.add(test_post_1)
        db.session.add(test_user_2)
        db.session.add(test_post_2)
        db.session.commit()
        yield app
        db.drop_all()


@pytest.fixture
def client(app_with_test_data_in_db):
    return app_with_test_data_in_db.test_client()


class UserActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, email="testUser1@gmail.com", password="Password1!"):
        return self._client.post(
            "/login", data=dict(email=email, password=password),
            follow_redirects=True)

    def logout(self):
        return self._client.get("/logout", follow_redirects=True)

    def register(self, username, email, password):
        return self._client.post(
            "/register", data=dict(username=username, email=email,
                                   password=password,
                                   confirm_password=password,
                                   follow_redirects=True))


@pytest.fixture
def authentication(client):
    return UserActions(client)
