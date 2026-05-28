import time
from typing import Callable, TypeVar

from playwright.sync_api import Page

T = TypeVar("T")


def retry(func: Callable[[], T], retries: int = 3, delay: float = 1.0) -> T:
    """Retry a callable up to n times, raising the last exception on exhaustion."""
    last_error: Exception = RuntimeError("retry called with zero retries")
    for attempt in range(retries):
        try:
            return func()
        except Exception as exc:
            last_error = exc
            if attempt < retries - 1:
                time.sleep(delay)
    raise last_error


def scroll_into_view(page: Page, selector: str) -> None:
    page.locator(selector).scroll_into_view_if_needed()


def wait_for_network_idle(page: Page, timeout: int = 5000) -> None:
    page.wait_for_load_state("networkidle", timeout=timeout)


def checkout_info() -> dict[str, str]:
    """Return a standard set of checkout form values for tests."""
    return {"first_name": "Test", "last_name": "User", "postal_code": "12345"}


def click_until_gone(
    page: Page,
    selector: str,
    timeout: int = 5000,
    max_clicks: int = 100,
) -> int:
    """
    Click an element repeatedly until it is no longer visible.

    Useful for "Show more" / "Load more" pagination buttons.
    Returns the number of clicks performed.
    Raises RuntimeError if the button is still present after max_clicks.
    """
    clicks = 0
    locator = page.locator(selector)

    while locator.is_visible():
        if clicks >= max_clicks:
            raise RuntimeError(
                f"'{selector}' still visible after {max_clicks} clicks — "
                "possible infinite loop, raise max_clicks if intentional."
            )
        locator.scroll_into_view_if_needed()
        locator.click()
        clicks += 1
        # Wait for network activity triggered by the click to settle,
        # then re-check visibility before the next iteration.
        try:
            page.wait_for_load_state("networkidle", timeout=timeout)
        except Exception:
            pass  # timeout is acceptable — element may already be gone

    return clicks
