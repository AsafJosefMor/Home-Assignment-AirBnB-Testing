import re
from config.selectors import (
    LISTING_CARDS_SELECTOR,
    LISTING_RATING_SELECTOR,
    LISTING_PRICE_SELECTOR,
    NEXT_PAGE_BUTTON_SELECTOR
)
from config.config import WAIT_AFTER_ACTION_MS
from pages.base_page import BasePage

"""
Page object for performing on Airbnb search results.
"""
class AirbnbResultPage(BasePage):
    def find_best_rated_cheapest_listing(self):
        """
        Analyze all paginated Airbnb listings to extract rating and price,
        select the best (highest rating, lowest price), and navigate to it.
        """
        all_listings = []
        current_page = 1

        # Step through each paginated result page
        while True:
            self.page.wait_for_timeout(WAIT_AFTER_ACTION_MS) # A lot of data needs to load in each page
            listings = self.page.locator(f"xpath={LISTING_CARDS_SELECTOR}")
            count = listings.count()
            self.log.info(f"Found {count} listings on page {current_page}")

            # Loop through each listing card on the current page
            for i in range(count):
                item = listings.nth(i)

                try:
                    # Extract rating and price
                    rating_text = item.locator(f"xpath={LISTING_RATING_SELECTOR}").inner_text(timeout=WAIT_AFTER_ACTION_MS)
                    price_text = item.locator(f"xpath={LISTING_PRICE_SELECTOR}").inner_text(timeout=WAIT_AFTER_ACTION_MS)
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
            next_button = self.page.locator(f"css={NEXT_PAGE_BUTTON_SELECTOR}")
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