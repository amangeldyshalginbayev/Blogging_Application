


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Home" in response.data
    assert b"About" in response.data
    assert b"Login" in response.data
    assert b"Register" in response.data

def test_home_page(client):
    response = client.get('/home')
    assert response.status_code == 200
    assert b"Home" in response.data
    assert b"About" in response.data
    assert b"Login" in response.data
    assert b"Register" in response.data

def test_about_page(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b"This blogging web application is built using Python and Flask by Amangeldy Shalginbayev" in response.data
