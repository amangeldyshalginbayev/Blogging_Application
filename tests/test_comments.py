def test_add_comment(app_with_test_data_in_db, client, authentication):
    with app_with_test_data_in_db.app_context():
        authentication.login()
        client.post("/post/1", data=dict(content="comment from test_user_1",
                                         follow_redirects=True))
        response = client.get("/post/1")
        assert response.status_code == 200
        assert b"comment from test_user_1" in response.data


def test_remove_comment(app_with_test_data_in_db, client, authentication):
    with app_with_test_data_in_db.app_context():
        authentication.login()
        client.post("/post/1", data=dict(content="comment from test_user_1",
                                         follow_redirects=True))
        response_after_adding_comment = client.get("/post/1")
        client.post("/comment/1",
                    data=dict(content="comment from test_user_1",
                              delete="Delete", follow_redirects=True))
        response_after_deleting_comment = client.get("/post/1")

        assert response_after_adding_comment.status_code == 200
        assert b"comment from test_user_1" in response_after_adding_comment.data

        assert response_after_deleting_comment.status_code == 200
        assert b"comment from test_user_1" not in response_after_deleting_comment.data


def test_update_comment(app_with_test_data_in_db, client, authentication):
    with app_with_test_data_in_db.app_context():
        authentication.login()
        client.post("/post/1", data=dict(content="comment from test_user_1",
                                         follow_redirects=True))
        response_after_adding_comment = client.get("/post/1")
        client.post("/comment/1",
                    data=dict(content="this is updated comment",
                              update="Update",
                              follow_redirects=True))
        response_after_updating_comment = client.get("/post/1")

        assert response_after_adding_comment.status_code == 200
        assert b"comment from test_user_1" in response_after_adding_comment.data

        assert response_after_updating_comment.status_code == 200
        assert b"comment from test_user_1" not in response_after_updating_comment.data
        assert b"this is updated comment" in response_after_updating_comment.data
