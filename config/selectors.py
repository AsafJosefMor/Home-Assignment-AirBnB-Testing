"""
Centralized Playwright selectors used across the automation framework.
Grouped by page to ensure clarity and maintainability.
"""

# ----------------------------------------
# Airbnb Search Page Selectors
# ----------------------------------------

# Input field for location (destination)
DESTINATION_INPUT_SELECTOR = '#bigsearch-query-location-input'

# Clickable area to open calendar for selecting check-in date
CHECKIN_SELECTOR = 'body > div:nth-child(6) > div > div > div > div > div > div > div > div > div > header > form > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(3) > div > div:nth-child(2)'

# Calendar selector to choose dates
CALENDAR_SELECTOR = 'button[data-state--date-string='

# Date picker selector start (need on add specific button dynamically to choose day of month)
DATE_PICKER_SELECTOR = '#panel--tabs--0 > div > div > div:nth-child(4) >div > div > div:nth-child(2)'

# Button to open the guest selection dropdown
WHO_BUTTON_SELECTOR = 'body > div:nth-child(6) > div > div > div > div > div > div > div > div > div > header > form > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(7) > div > div > div > div'

# Search execution button (requires deep CSS due to Airbnb's React structure)
SEARCH_BUTTON_SELECTOR = 'body > div:nth-child(6) > div > div > div > div > div > div > div > div > div > header > form > div > div > div:nth-child(2) > div:nth-child(3) > button'

# "+" button to add one adult to the guest count
ADULTS_PLUS_SELECTOR = '#stepper-adults > button:nth-child(3)'

# "+" button to add one child to the guest count
CHILDREN_PLUS_SELECTOR = '#stepper-children > button:nth-child(3)'

# Locator showing current search location (used for assertion)
LOCATION_SUMMARY_SELECTOR = 'body > div:nth-child(6) > div > div > div > div > div > div:nth-child(2) > header > div > div > div > div > div > form > div > div > div:nth-child(2) > div > div:nth-child(3) > button:nth-child(1) > div:nth-child(3)'

# Locator showing current guests (used for assertion)
GUESTS_SUMMARY_SELECTOR = "#react-application > div > div > div:nth-child(1) > div > div > div > header > div > div > div > div > div > form > div > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > button:nth-child(5) > div:nth-child(3)"

# ----------------------------------------
# Airbnb Results Page Selectors
# ----------------------------------------

# Next page button
NEXT_PAGE_BUTTON = '#site-content > div > div > div > div > div > nav > div > a:last-child'

# Container for each search result item
LISTING_CARDS_SELECTOR = '//div[@data-testid="card-container"]'

# Price display element inside listing cards
LISTING_PRICE_SELECTOR = './/span[contains(text(), " per night")]'

# Star rating label associated with a listing
LISTING_RATING_SELECTOR = './/span[@aria-hidden="true" and contains(text(), " (")]'

# Pagination next button
NEXT_PAGE_BUTTON_SELECTOR = '#site-content > div > div > div > div > div > nav > div > a:last-child'

# ----------------------------------------
# Airbnb Reservation Page Selectors
# ----------------------------------------

# Reserve button
RESERVE_BUTTON_SELECTOR = '#site-content > div > div:nth-child(1) > div:nth-child(3) > div > div > div > div > div:nth-child(1) > div > div > div > div:nth-child(2) > div > div > div> div> div > button'

# Guests data
GUESTS_INFO_SELECTOR = '#site-content > div > div > div > div:nth-child(1) > div > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div:nth-child(1) > div:nth-child(2) > div:nth-child(2)'

# Dates data
CHECKIN_CHECKOUT_DATE_SELECTOR = '#site-content > div > div > div > div:nth-child(1) > div > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)'

# Next button
RESERVATION_NEXT_BUTTON_SELECTOR = '#site-content > div > div > div > div:nth-child(1) > div > div:nth-child(2) > div > div > div:nth-child(1) > div > div > button'

# Phone input
PHONE_INPUT_SELECTOR = '#phoneInputphone-login'

# Final continue button in phone input pop-up
FINAL_CONTINUE_BUTTON_SELECTOR = 'body > div:nth-child(16) > div > section > div > div > div > div > div > div > form > div > div > button'

# Close button for translation pop-up on the reservation page (if present)
TRANSLATION_POPUP_CLOSE_BUTTON = 'div > div > section > div > div > div:nth-child(2)> div > div > button'
