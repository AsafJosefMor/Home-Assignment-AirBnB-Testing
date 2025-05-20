"""
BasePage: Reusable utilities for page interactions.
"""
from utils.logging_utils import get_logger

class BasePage:
    def __init__(self, page):
        self.page = page
        self.log = get_logger(self.__class__.__name__)
