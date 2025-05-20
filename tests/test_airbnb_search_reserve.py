"""
test_airbnb_search_reserve.py:
Main end-to-end test for search, result filtering, and reservation on Airbnb.
"""
import json
import os
import pytest
from config.config import BASE_URL, WAIT_AFTER_ACTION_MS

from pages.airbnb_search_page import AirbnbSearchPage
from pages.airbnb_result_page import AirbnbResultPage
from pages.airbnb_reservation_page import AirbnbReservationPage

# Load test data from config directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(BASE_DIR, "config", "test_data.json")) as f:
    TEST_CASES = [json.load(f)]

@pytest.mark.parametrize("test_data", TEST_CASES)
def test_airbnb_search_reserve(page, test_data):
    """
    Executes Airbnb test flow:
    1. Perform search
    2. Analyze listings
    3. Reserve best option (Highest ranked, lowest priced)
    4. Assert expected test data
    """

    # Start browser with base URL
    page.goto(BASE_URL)
    page.wait_for_timeout(WAIT_AFTER_ACTION_MS)

    # Load search parameters from test data
    location = test_data["location"]
    checkin = test_data["checkin"]
    checkout = test_data["checkout"]
    adults = test_data["adults"]
    children = test_data["children"]

    # Group guest data into a dictionary for validation
    guests = {
        "adults": test_data["adults"],
        "children": test_data["children"]
    }

    # Perform search
    search_page = AirbnbSearchPage(page)
    search_page.search(location, checkin, checkout, adults, children)

    # Validate search results against parameters
    search_page.validate_search(location, checkin, checkout, guests)

    # Result analysis
    results = AirbnbResultPage(page)
    best = results.find_best_rated_cheapest_listing()
    assert best, "No valid listings found."
    assert best["price"] > 0, "Listing price must be positive."

    # Create a "temp" directory to save output in
    temp_dir = os.path.join(BASE_DIR, "temp")
    os.makedirs(temp_dir, exist_ok=True)

    # Log and save best listing result to a file
    result_path = os.path.join(temp_dir, "best_listing.json")
    with open(result_path, "w") as f:
        json.dump(best, f, indent=2)

    # Reservation
    reserve = AirbnbReservationPage(page)
    result = reserve.reserve(test_data["phone"])

    # Save reservation details to a file
    result_path = os.path.join(temp_dir, "post_reservation_details.json")
    with open(result_path, "w") as f:
        json.dump(result, f, indent=2)

    # Assert reservation data
    assert result["guest_counts"]["adults"] == test_data["adults"]
    assert result["guest_counts"]["children"] == test_data["children"]
    assert "airbnb" in result["url"]