from flaskblog import create_app, create_test_app


def test_production_app_config():
    assert not create_app().testing


def test_test_app_config():
    assert create_test_app().testing
