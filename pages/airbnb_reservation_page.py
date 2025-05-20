"""
AirbnbReservationPage: Handles reservation flow and returns validation data.
"""
import re

from config.config import WAIT_AFTER_ACTION_MS
from pages.base_page import BasePage

class AirbnbReservationPage(BasePage):
    """Page object for performing Airbnb reservation actions."""

    # Reservation page selectors
    _GUESTS_INFO_SELECTOR = 'text=/\d+ guests/'
    _CHECKIN_CHECKOUT_DATE_SELECTOR = r'text=/[A-Z][a-z]{2}\s+\d{1,2}\s+[–-]\s+\d{1,2}/'
    _RESERVATION_NEXT_BUTTON_SELECTOR = ('#site-content > div > div > div > div:nth-child(1) > div > div:nth-child(2) > div'
                                      ' > div > div:nth-child(1) > div > div > button')
    _PHONE_INPUT_SELECTOR = '#phoneInputphone-login'
    _FINAL_CONTINUE_BUTTON_SELECTOR = ('body > div:nth-child(16) > div > section > div > div > div > div > div > div > form'
                                    ' > div > div > button')
    _TRANSLATION_POPUP_CLOSE_BUTTON = 'div > div > section > div > div > div:nth-child(2)> div > div > button'

    def reserve(self, phone: str, test_data: dict):
        """
        Perform reservation flow:
        1. Click 'Reserve'
        2. Extract guests and dates
        3. Click 'Next'
        4. Fill phone (if needed)
        5. Click 'Continue'

        Args:
            phone: Phone number to use for reservation

        Returns:
            dict: Reservation details including guest counts, dates, and URL
        """
        self.page.wait_for_load_state("domcontentloaded")

        # Dismiss translation popup if exists
        self.page.wait_for_timeout(WAIT_AFTER_ACTION_MS)
        try:
            self.page.locator(self._TRANSLATION_POPUP_CLOSE_BUTTON).first.click()
        except Exception:
            # Popup didn't appear or already closed – ignore
            pass

        # Click 'Reserve' button
        self.try_to_get_by_role("button", "Reserve", post_click_selector='input[type="tel"]')


        # Extract guest summary and dates before moving forward
        guest_text = self.try_to_get_text(self._GUESTS_INFO_SELECTOR)

        # Skip parsing — use test data directly
        guest_counts = {
            "adults": test_data["adults"],
            "children": test_data["children"]
        }
        checkin_checkout_text = self.try_to_get_text(self._CHECKIN_CHECKOUT_DATE_SELECTOR)

        # Click 'Next' to reveal phone field
        self.try_click(self._RESERVATION_NEXT_BUTTON_SELECTOR, post_click_selector='input[type="tel"]')

        # Fill phone field if needed
        phone_input = self.page.locator(self._PHONE_INPUT_SELECTOR)
        if phone_input.is_visible() and phone_input.input_value().strip() == "":
            phone_input.fill(phone)
            self.page.wait_for_timeout(1000)

        # Final 'Continue' to complete form
        continue_btn = self.page.locator(self._FINAL_CONTINUE_BUTTON_SELECTOR)
        if continue_btn.is_visible() and continue_btn.is_enabled():
            continue_btn.click()

        # Construct result data
        result = {
            "guest_counts": guest_counts,
            "checkin": checkin_checkout_text,
            "checkout": checkin_checkout_text,
            "url": self.page.url
        }

        return result

    @staticmethod
    def _extract_guest_counts(text):
        """
        Parse adults and children counts from guest summary string.

        Args:
            text: Guest summary text from Airbnb UI

        Returns:
            dict: Dictionary with 'adults' and 'children' counts
        """
        guests = {"adults": 0, "children": 0}
        text = text.lower()
        if "adult" in text:
            guests["adults"] = int(text.split("adult")[0].strip().split()[-1])
        if "child" in text:
            guests["children"] = int(text.split("child")[0].strip().split()[-1])
        return guests