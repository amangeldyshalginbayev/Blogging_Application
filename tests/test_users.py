def test_login(client, authentication):
    # test that viewing the page renders without template errors
    assert client.get("/login").status_code == 200

    with client:
        response = authentication.login()
        assert response.status_code == 200
        assert b"Login" not in response.data
        assert b"Welcome back, testUser1!" in response.data


def test_logout(client, authentication):
    authentication.login()

    with client:
        response = authentication.logout()
        assert response.status_code == 200
        assert b"Login" in response.data
        assert b"Register" in response.data
        assert b"Logout" not in response.data


def test_login_with_invalid_password(client, authentication):
    response = authentication.login(password="invalid_password")

    assert response.status_code == 200
    assert b"Login Unsuccessful. Please check email and password" \
           in response.data


def test_login_with_user_that_doesnt_exist(client, authentication):
    response = authentication.login(email="nosuchuser@gmail.com")

    assert response.status_code == 200
    assert b"Login Unsuccessful. Please check email and password" \
           in response.data


def test_register_new_user_with_email_and_username_that_already_registered(
        authentication):
    response = authentication.register(username="testUser1",
                                       email="testUser1@gmail.com",
                                       password="Letmein1!")

    assert response.status_code == 200
    assert b"That username is taken. Please choose a different one." \
           in response.data
    assert b"That email is taken. Please choose a different one." \
           in response.data


def test_like(app_with_test_data_in_db, client, authentication):
    with app_with_test_data_in_db.app_context():
        authentication.login()
        response_with_no_likes = client.get("/post/1")
        response_with_like = client.get("/like/1/like", follow_redirects=True)

        assert response_with_no_likes.status_code == 200
        assert b"This post has not been liked yet. Like it!" in response_with_no_likes.data

        assert response_with_like.status_code == 200
        assert b"You liked the post!" in response_with_like.data
        assert b"This post has been liked <b>1</b> times." in response_with_like.data
