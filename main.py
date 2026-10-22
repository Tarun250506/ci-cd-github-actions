
from fastapi import FastAPI, HTTPException
import requests

app = FastAPI(title="Public Holiday Finder")

API_URL = "https://date.nager.at/api/v3"


@app.get("/")
def home():
    return {"message": "Public Holiday Finder is running!"}


@app.get("/holidays/{year}/{country_code}")
def get_holidays(year: int, country_code: str):
    if year < 1900 or year > 2100:
        raise HTTPException(
            status_code=400,
            detail="Year must be between 1900 and 2100"
        )

    country_code = country_code.upper()

    if len(country_code) != 2 or not country_code.isalpha():
        raise HTTPException(
            status_code=400,
            detail="Country code must contain two letters"
        )

    try:
        response = requests.get(
            f"{API_URL}/PublicHolidays/{year}/{country_code}",
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException:
        raise HTTPException(
            status_code=502,
            detail="Could not retrieve holiday data"
        )
