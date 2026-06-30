from app import create_app


def test_talibes_page_loads():
    app = create_app("development")
    app.config.update(TESTING=True)

    with app.test_client() as client:
        response = client.get("/talibes/")

    assert response.status_code == 200
