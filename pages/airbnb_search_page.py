"""
Performs Airbnb search actions using Playwright.
"""
from urllib.parse import urlparse, parse_qs
from config.config import WAIT_AFTER_ACTION_MS
from pages.base_page import BasePage

class AirbnbSearchPage(BasePage):
    """
    Page object for performing Airbnb searches.
    Handles search flow on Airbnb including destination, dates, and guests.
    """

    # Search form selectors
    _DESTINATION_INPUT_SELECTOR = '#bigsearch-query-location-input'
    _CHECKIN_SELECTOR = ('body > div:nth-child(6) > div > div > div > div > div > div > div > div > div > header > form >'
                      ' div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(3) > div > div:nth-child(2)')
    _CALENDAR_SELECTOR = 'button[data-state--date-string='
    _DATE_PICKER_SELECTOR = '#panel--tabs--0 > div > div > div:nth-child(4) >div > div > div:nth-child(2)'
    _WHO_BUTTON_SELECTOR = ('body > div:nth-child(6) > div > div > div > div > div > div > div > div > div > header > form >'
                         ' div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(7) > div > div > div > div')
    _SEARCH_BUTTON_SELECTOR = ('body > div:nth-child(6) > div > div > div > div > div > div > div > div > div > header > form'
                            ' > div > div > div:nth-child(2) > div:nth-child(3) > button')

    # Guest count selectors
    _ADULTS_PLUS_SELECTOR = '#stepper-adults > button:nth-child(3)'
    _CHILDREN_PLUS_SELECTOR = '#stepper-children > button:nth-child(3)'

    # Validation selectors
    _LOCATION_SUMMARY_SELECTOR = ('body > div:nth-child(6) > div > div > div > div > div > div:nth-child(2) > header > div >'
                               ' div > div > div > div > form > div > div > div:nth-child(2) > div > div:nth-child(3) >'
                               ' button:nth-child(1) > div:nth-child(3)')
    _GUESTS_SUMMARY_SELECTOR = ("#react-application > div > div > div:nth-child(1) > div > div > div > header > div > div >"
                             " div > div > div > form > div > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(3)"
                             " > button:nth-child(5) > div:nth-child(3)")

    # Results page selector for validation
    _LISTING_CARDS_SELECTOR = '//div[@data-testid="card-container"]'

    def __init__(self, page):
        """
        Initialize AirbnbSearchPage.

        Args:
            page: Playwright page object
        """
        super().__init__(page)

    def search(self, location: str, checkin: str, checkout: str, adults: int, children: int):
        """
        Perform a search on Airbnb with the given parameters.

        Args:
            location: Destination location
            checkin: Check-in date in format expected by Airbnb
            checkout: Check-out date in format expected by Airbnb
            adults: Number of adult guests
            children: Number of child guests

        Returns:
            None
        """
        self.page.wait_for_load_state("domcontentloaded")

        # Fill destination
        self.try_click(self._DESTINATION_INPUT_SELECTOR, 5, 1500, True)
        self.page.locator(self._DESTINATION_INPUT_SELECTOR).fill(location)
        self.page.wait_for_timeout(WAIT_AFTER_ACTION_MS)

        # Click dates
        self.try_click(self._CHECKIN_SELECTOR)
        self.page.wait_for_timeout(WAIT_AFTER_ACTION_MS)
        self.page.locator(f'{self._CALENDAR_SELECTOR}"{checkin}"]').first.click()
        self.page.wait_for_timeout(WAIT_AFTER_ACTION_MS)
        self.page.locator(f'{self._CALENDAR_SELECTOR}"{checkout}"]').first.click()
        self.page.wait_for_timeout(WAIT_AFTER_ACTION_MS)

        # Click number of guests
        self.try_click(self._WHO_BUTTON_SELECTOR)
        self.page.wait_for_timeout(WAIT_AFTER_ACTION_MS)
        for _ in range(adults):
            self.page.locator(self._ADULTS_PLUS_SELECTOR).first.click()
        self.page.wait_for_timeout(WAIT_AFTER_ACTION_MS)
        for _ in range(children):
            self.page.locator(self._CHILDREN_PLUS_SELECTOR).first.click()

        # Click search button
        self.try_click(self._SEARCH_BUTTON_SELECTOR)
        self.page.wait_for_timeout(WAIT_AFTER_ACTION_MS)

        self.log.info(f"Search completed.")

    def validate_search(self, location: str, checkin: str, checkout: str, guests: dict):
        """
        Validate that the search results match the search criteria.

        Args:
            location: Expected location in results
            checkin: Expected check-in date
            checkout: Expected check-out date
            guests: Dictionary with 'adults' and 'children' keys

        Returns:
            None

        Raises:
            AssertionError: If validation fails
        """
        self.log.info(f"Validating search.")

        # --- Validate location in UI ---
        summary_text = self.page.locator(self._LOCATION_SUMMARY_SELECTOR).first.inner_text()
        assert summary_text.endswith(location), f"Expected location to end with '{location}', got '{summary_text}'"

        # --- Validate total guest count in UI ---
        guests_text = self.page.locator(self._GUESTS_SUMMARY_SELECTOR).first.inner_text()
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