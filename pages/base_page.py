"""
BasePage: Reusable utilities for page interactions.
"""
from config.config import WAIT_AFTER_ACTION_MS
from utils.logging_utils import get_logger

class BasePage:
    """Base class for all page objects with common functionality."""

    def __init__(self, page):
        """
        Initialize the base page object.

        Args:
            page: Playwright page object
        """
        self.page = page
        self.log = get_logger(self.__class__.__name__)

    def try_click(self, locator, retries=5, delay_ms=WAIT_AFTER_ACTION_MS, with_refresh=False,
                  post_click_selector=None):
        for attempt in range(retries):
            try:
                # Early escape: if post-click element is already there, skip the click
                if post_click_selector:
                    try:
                        if self.page.locator(post_click_selector).is_visible():
                            return
                    except:
                        pass

                element = self.page.locator(locator)
                element.wait_for(state="visible", timeout=WAIT_AFTER_ACTION_MS)
                element.click()

                # Wait for result of click if applicable
                if post_click_selector:
                    self.page.locator(post_click_selector).wait_for(state="visible", timeout=WAIT_AFTER_ACTION_MS)

                return
            except Exception as e:
                if with_refresh:
                    self.page.reload()
                self.page.wait_for_timeout(WAIT_AFTER_ACTION_MS)

                if attempt == retries - 1:
                    raise e

                self.page.wait_for_timeout(delay_ms)

    def try_to_get_by_role(self, element_type, name, retries=5, delay_ms=WAIT_AFTER_ACTION_MS,
                           post_click_selector=None):
        for attempt in range(retries):
            try:
                # Check first: has the click already succeeded?
                if post_click_selector:
                    try:
                        if self.page.locator(post_click_selector).is_visible():
                            return
                    except:
                        pass

                element = self.page.get_by_role(element_type, name=name)
                element.wait_for(state="visible", timeout=WAIT_AFTER_ACTION_MS)
                element.click()

                if post_click_selector:
                    self.page.locator(post_click_selector).wait_for(state="visible", timeout=WAIT_AFTER_ACTION_MS)

                return
            except Exception as e:
                if attempt == retries - 1:
                    raise e
                self.page.wait_for_timeout(delay_ms)


    def try_to_get_text(self, locator, retries=5, delay_ms=WAIT_AFTER_ACTION_MS):
        for attempt in range(retries):
            try:
                element = self.page.locator(locator)
                element.wait_for(state="attached", timeout=WAIT_AFTER_ACTION_MS)  # safer than 'visible'
                return element.inner_text()
            except Exception as e:
                if attempt == retries - 1:
                    raise e
                self.page.wait_for_timeout(delay_ms)
        return None