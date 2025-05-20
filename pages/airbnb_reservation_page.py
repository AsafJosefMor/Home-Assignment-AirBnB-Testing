"""
AirbnbReservationPage: Completes reservation and returns validation data.
"""

from config.config import WAIT_AFTER_ACTION_MS
from pages.base_page import BasePage
from config.selectors import (
    RESERVE_BUTTON_SELECTOR,
    PHONE_INPUT_SELECTOR,
    GUESTS_INFO_SELECTOR,
    CHECKIN_CHECKOUT_DATE_SELECTOR,
    RESERVATION_NEXT_BUTTON_SELECTOR,
    FINAL_CONTINUE_BUTTON_SELECTOR,
    TRANSLATION_POPUP_CLOSE_BUTTON
)

"""
Page object for performing on Airbnb reservation.
"""
class AirbnbReservationPage(BasePage):
    def reserve(self, phone: str):
        """
        Perform reservation flow:
        1. Click 'Reserve'
        2. Extract guests and dates
        3. Click 'Next'
        4. Fill phone (if needed)
        5. Click 'Continue'
        """

        # Dismiss translation popup if exist
        self.page.wait_for_timeout(WAIT_AFTER_ACTION_MS)
        try:
            self.page.locator(TRANSLATION_POPUP_CLOSE_BUTTON).first.click()
            self.page.wait_for_timeout(WAIT_AFTER_ACTION_MS)
        except Exception:
            # Popup didn’t appear or already closed – ignore
            pass

        # Click 'Reserve' button
        reserve_btn = self.page.locator(RESERVE_BUTTON_SELECTOR).first
        reserve_btn.click()
        self.page.wait_for_timeout(WAIT_AFTER_ACTION_MS)

        # Extract guest summary and dates before moving forward
        guest_text = self.page.locator(GUESTS_INFO_SELECTOR).inner_text(timeout=WAIT_AFTER_ACTION_MS)
        guest_counts = extract_guest_counts(guest_text)
        checkin_text = self.page.locator(CHECKIN_CHECKOUT_DATE_SELECTOR).inner_text(timeout=WAIT_AFTER_ACTION_MS)
        checkout_text = self.page.locator(CHECKIN_CHECKOUT_DATE_SELECTOR).inner_text(timeout=WAIT_AFTER_ACTION_MS)

        # Click 'Next' to reveal phone field
        next_btn = self.page.locator(RESERVATION_NEXT_BUTTON_SELECTOR)
        if next_btn.is_visible() and next_btn.is_enabled():
            next_btn.click()
            self.page.wait_for_timeout(1000)

        # Fill phone field if needed
        phone_input = self.page.locator(PHONE_INPUT_SELECTOR)
        if phone_input.is_visible() and phone_input.input_value().strip() == "":
            phone_input.fill(phone)
            self.page.wait_for_timeout(1000)

        # Final 'Continue' to complete form
        continue_btn = self.page.locator(FINAL_CONTINUE_BUTTON_SELECTOR)
        if continue_btn.is_visible() and continue_btn.is_enabled():
            continue_btn.click()

        # Construct result data
        result = {
            "guest_counts": guest_counts,
            "checkin": checkin_text,
            "checkout": checkout_text,
            "url": self.page.url
        }

        return result

def extract_guest_counts(text):
    """
    Parse adults and children counts from guest summary string.
    """
    guests = {"adults": 0, "children": 0}
    text = text.lower()
    if "adult" in text:
        guests["adults"] = int(text.split("adult")[0].strip().split()[-1])
    if "child" in text:
        guests["children"] = int(text.split("child")[0].strip().split()[-1])
    return guests