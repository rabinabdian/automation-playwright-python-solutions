import pytest
from playwright.sync_api import Page, APIRequestContext

from pages.login_page import LoginPage

STANDARD_USER = "standard_user"
PASSWORD = "secret_sauce"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
    }


@pytest.fixture
def logged_in_page(page: Page) -> Page:
    """Return a page already authenticated into SauceDemo."""
    login = LoginPage(page)
    login.open()
    login.login(STANDARD_USER, PASSWORD)
    page.wait_for_url("**/inventory.html")
    return page


@pytest.fixture(scope="session")
def api_context(playwright) -> APIRequestContext:
    """Session-scoped Playwright API request context for JSONPlaceholder."""
    context = playwright.request.new_context(
        base_url="https://jsonplaceholder.typicode.com",
        extra_http_headers={"Content-Type": "application/json"},
    )
    yield context
    context.dispose()
