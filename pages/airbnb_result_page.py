"""
Page object for performing actions on Airbnb search results.
"""
import re
from config.config import WAIT_AFTER_ACTION_MS
from pages.base_page import BasePage


class AirbnbResultPage(BasePage):
    """Page object for analyzing and interacting with Airbnb search results."""

    # Search result page selectors
    _LISTING_CARDS_SELECTOR = '//div[@data-testid="card-container"]'
    _LISTING_RATING_SELECTOR = './/span[@aria-hidden="true" and contains(text(), " (")]'
    _LISTING_PRICE_SELECTOR = './/span[contains(text(), " per night")]'
    _NEXT_PAGE_BUTTON_SELECTOR = '#site-content > div > div > div > div > div > nav > div > a:last-child'

    def find_best_rated_cheapest_listing(self):
        """
        Analyze all paginated Airbnb listings to extract rating and price,
        select the best (highest rating, lowest price), and navigate to it.

        Returns:
            dict: Details of the selected best listing

        Raises:
            AssertionError: If no listings are found
        """
        all_listings = []
        current_page = 1

        # Step through each paginated result page
        while True:
            self.page.wait_for_timeout(WAIT_AFTER_ACTION_MS)
            listings = self.page.locator(f"xpath={self._LISTING_CARDS_SELECTOR}")
            count = listings.count()
            self.log.info(f"Found {count} listings on page {current_page}")

            # Loop through each listing card on the current page
            for i in range(count):
                item = listings.nth(i)

                try:
                    # Extract rating and price
                    rating_text = item.locator(f"xpath={self._LISTING_RATING_SELECTOR}").inner_text(
                        timeout=WAIT_AFTER_ACTION_MS)
                    price_text = item.locator(f"xpath={self._LISTING_PRICE_SELECTOR}").inner_text(
                        timeout=WAIT_AFTER_ACTION_MS)
                    rating = float(rating_text.strip().split()[0])
                    price = int(re.sub(r"\D", "", price_text))
                except Exception as e:
                    continue

                # Extract listing URL from anchor element
                anchors = item.locator("a")
                hrefs = anchors.evaluate_all("els => els.map(el => el.getAttribute('href'))")
                if not hrefs or not hrefs[0]:
                    self.log.warning(f"No href in listing {i}. Skipping.")
                    continue

                full_url = self.page.url.split("/s/")[0] + hrefs[0]

                # Append listing data to list
                all_listings.append({
                    "rank": len(all_listings) + 1,
                    "index": i,
                    "rating": rating,
                    "price": price,
                    "url": full_url,
                    "title": item.inner_text().strip()
                })

            # Check for and click the pagination next button
            next_button = self.page.locator(f"css={self._NEXT_PAGE_BUTTON_SELECTOR}")
            if next_button.count() > 0 and next_button.first.is_enabled():
                next_button.first.click()
                current_page += 1
            else:
                break

        if not all_listings:
            raise AssertionError("No listings found")

        # Choose the best listing: highest rating, lowest price
        max_rating = max(l["rating"] for l in all_listings)
        top = [l for l in all_listings if l["rating"] == max_rating]
        best_listing = sorted(top, key=lambda x: x["price"])[0]

        # Navigate to best listing
        self.page.goto(best_listing["url"])
        self.log.info(f"Navigated to best listing: {best_listing['url']}")

        return best_listing