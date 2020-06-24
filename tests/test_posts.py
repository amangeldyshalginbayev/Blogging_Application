def test_index_page_posts(client):
    response = client.get("/")
    assert b"test_title1" in response.data
    assert b"test_content1" in response.data
    assert b"testUser1" in response.data
    assert b"2013-10-12" in response.data

    assert b"test_title2" in response.data
    assert b"test_content2" in response.data
    assert b"testUser2" in response.data


def test_create(client, authentication, app_with_test_data_in_db):
    with app_with_test_data_in_db.app_context():
        authentication.login()
        assert client.get("/post/new").status_code == 200
        client.post("/post/new", data=dict(title="New Post Title",
                                           content="New Post Content",
                                           follow_redirects=True))
        index_page = client.get("/")
        assert b"New Post Title" in index_page.data
        assert b"New Post Content" in index_page.data


def test_update(app_with_test_data_in_db, authentication, client):
    with app_with_test_data_in_db.app_context():
        authentication.login()
        assert client.get("/post/1/update").status_code == 200
        client.post("/post/1/update", data=dict(title="New Updated Title",
                                                content="New Updated Content",
                                                follow_redirects=True))
        index_page = client.get("/")
        assert b"New Updated Title" in index_page.data
        assert b"New Updated Content" in index_page.data


def test_delete(app_with_test_data_in_db, authentication, client):
    with app_with_test_data_in_db.app_context():
        authentication.login()
        client.post("/post/1/delete", data=dict(title="New Updated Title",
                                                content="New Updated Content",
                                                follow_redirects=True))
        index_page = client.get("/")
        assert b"test_title1" not in index_page.data
        assert b"test_content1" not in index_page.data


def test_user_can_not_update_other_users_post(app_with_test_data_in_db,
                                              authentication, client):
    with app_with_test_data_in_db.app_context():
        authentication.login()
        client.get("/post/2/update").status_code == 403


def test_user_can_not_delete_other_users_post(app_with_test_data_in_db,
                                              authentication, client):
    with app_with_test_data_in_db.app_context():
        authentication.login()
        client.post("/post/2/delete").status_code == 403
