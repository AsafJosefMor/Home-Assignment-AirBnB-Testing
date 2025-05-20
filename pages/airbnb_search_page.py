"""
Performs Airbnb search actions using Playwright and selectors.
"""
from config.config import WAIT_AFTER_ACTION_MS
from pages.base_page import BasePage
from config.selectors import *
from urllib.parse import urlparse, parse_qs

"""
Page object for performing Airbnb searches.
Handles search flow on Airbnb including destination, dates, and guests.
"""
class AirbnbSearchPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    """
    Perform a search and return the guest summary text for validation.
    """
    def search(self, location: str, checkin: str, checkout: str, adults: int, children: int):

        # Fill destination
        self.page.locator(DESTINATION_INPUT_SELECTOR).wait_for(timeout=WAIT_AFTER_ACTION_MS)
        self.page.locator(DESTINATION_INPUT_SELECTOR).click()
        self.page.locator(DESTINATION_INPUT_SELECTOR).fill(location)
        self.page.wait_for_timeout(WAIT_AFTER_ACTION_MS)

        # Click dates
        self.page.locator(CHECKIN_SELECTOR).wait_for(timeout=WAIT_AFTER_ACTION_MS)
        self.page.locator(CHECKIN_SELECTOR).click()
        self.page.wait_for_timeout(WAIT_AFTER_ACTION_MS)
        self.page.locator(f'{CALENDAR_SELECTOR}"{checkin}"]').first.click()
        self.page.wait_for_timeout(WAIT_AFTER_ACTION_MS)
        self.page.locator(f'{CALENDAR_SELECTOR}"{checkout}"]').first.click()
        self.page.wait_for_timeout(WAIT_AFTER_ACTION_MS)

        # Click number of guests
        self.page.locator(WHO_BUTTON_SELECTOR).wait_for(timeout=WAIT_AFTER_ACTION_MS)
        self.page.locator(WHO_BUTTON_SELECTOR).click()
        self.page.wait_for_timeout(WAIT_AFTER_ACTION_MS)
        for _ in range(adults):
            self.page.locator(ADULTS_PLUS_SELECTOR).first.click()
        self.page.wait_for_timeout(WAIT_AFTER_ACTION_MS)
        for _ in range(children):
            self.page.locator(CHILDREN_PLUS_SELECTOR).first.click()

        # Click search button
        self.page.locator(SEARCH_BUTTON_SELECTOR).wait_for(timeout=WAIT_AFTER_ACTION_MS)
        self.page.locator(SEARCH_BUTTON_SELECTOR).click()

        # Wait for listing cards to appear
        self.page.wait_for_selector(LISTING_CARDS_SELECTOR, timeout=10000)

        self.log.info("Search completed and validated for location: " + location)

    def validate_search(self, location: str, checkin: str, checkout: str, guests: dict):
        # --- Validate location in UI ---
        summary_text = self.page.locator(LOCATION_SUMMARY_SELECTOR).first.inner_text()
        assert summary_text.endswith(location), f"Expected location to end with '{location}', got '{summary_text}'"

        # --- Validate total guest count in UI ---
        guests_text = self.page.locator(GUESTS_SUMMARY_SELECTOR).first.inner_text()
        expected_guests_count = sum(guests.values())
        assert str(expected_guests_count) in guests_text, \
            f"Expected total guests '{expected_guests_count}', got '{guests_text}'"

        # --- Validate query parameters in URL ---
        parsed_url = urlparse(self.page.url)
        query_params = parse_qs(parsed_url.query)

        def assert_url_param(param, expected):
            actual = query_params.get(param, [None])[0]
            assert str(actual) == str(expected), f"Expected URL param '{param}={expected}', got '{actual}'"

        assert_url_param("adults", guests.get("adults", 0))
        assert_url_param("children", guests.get("children", 0))
        assert_url_param("checkin", checkin)
        assert_url_param("checkout", checkout)