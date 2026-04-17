def test_register_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "password": "testpassword",
            "invite_code": "0168",
        },
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


def test_login_user(client):
    response = client.post(
        "/api/v1/auth/login", json={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
