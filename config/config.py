import os
from dotenv import load_dotenv

"""
Environment & Defaults
"""

load_dotenv()
BASE_URL = os.getenv("BASE_URL", "https://www.airbnb.com")
WAIT_AFTER_ACTION_MS = int(os.getenv("WAIT_AFTER_ACTION_MS", 4000))
SUITE_TIMEOUT_SEC = int(os.getenv("SUITE_TIMEOUT_SEC", 900))  # in seconds
