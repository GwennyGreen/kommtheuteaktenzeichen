"""Runner script for web scraping"""

from kha import scraper


def run() -> None:
    """Runs the scraper and prints the results."""
    for episode in scraper.scrape_wunschliste():
        print(repr(episode))
