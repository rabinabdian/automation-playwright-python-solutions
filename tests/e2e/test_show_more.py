import pytest
from playwright.sync_api import Page

from utils.helpers import click_until_gone

SHOW_MORE_SELECTOR = "button.button.button-round.button-primary.button-bold.button-big"


@pytest.mark.e2e
def test_click_show_more_until_gone(page: Page):
    """
    Demonstrates click_until_gone() — keeps clicking 'Show more jobs'
    until the button disappears (all results loaded).

    Replace the URL below with the actual jobs page you are testing.
    """
    page.goto("https://example-jobs-site.com/jobs")  # <-- swap in the real URL
    page.wait_for_load_state("networkidle")

    button = page.locator(SHOW_MORE_SELECTOR)

    # If the button is not present at all, there is only one page of results.
    if not button.is_visible():
        pytest.skip("No 'Show more jobs' button found — single page of results")

    clicks = click_until_gone(page, SHOW_MORE_SELECTOR)

    assert not button.is_visible(), "Button should be gone after exhausting all pages"
    assert clicks > 0
    print(f"Clicked 'Show more jobs' {clicks} time(s) to load all results")
