def test_check_draw(client):
    response = client.post(
        "/api/v1/check/draw",
        json={
            "ticket_reds": [1, 2, 3, 4, 5, 6],
            "ticket_blues": [7],
            "period": "2023001",
        },
    )
    assert response.status_code == 200
    assert response.json()["prize_level"] == 1
