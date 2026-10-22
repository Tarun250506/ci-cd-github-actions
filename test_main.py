
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Public Holiday Finder is running!"
    }


@patch("main.requests.get")
def test_get_holidays_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {
            "date": "2026-07-04",
            "localName": "Independence Day",
            "name": "Independence Day",
            "countryCode": "US"
        }
    ]
    mock_get.return_value.raise_for_status.return_value = None

    response = client.get("/holidays/2026/US")

    assert response.status_code == 200
    assert response.json()[0]["name"] == "Independence Day"
    mock_get.assert_called_once()


def test_invalid_year():
    response = client.get("/holidays/1800/US")
    assert response.status_code == 400


def test_invalid_country_code():
    response = client.get("/holidays/2026/USA")
    assert response.status_code == 400


@patch("main.requests.get")
def test_external_api_failure(mock_get):
    import requests

    mock_get.side_effect = requests.Timeout("API timed out")

    response = client.get("/holidays/2026/US")

    assert response.status_code == 502
    assert response.json()["detail"] == (
        "Could not retrieve holiday data"
    )
