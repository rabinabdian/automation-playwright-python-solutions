import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.products_page import ProductsPage

VALID_USER = "standard_user"
VALID_PASSWORD = "secret_sauce"


@pytest.mark.e2e
@pytest.mark.smoke
def test_successful_login_redirects_to_products(page: Page):
    login = LoginPage(page)
    login.open().login(VALID_USER, VALID_PASSWORD)

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    products = ProductsPage(page)
    assert products.is_loaded()


@pytest.mark.e2e
def test_login_with_wrong_password_shows_error(page: Page):
    login = LoginPage(page)
    login.open().login(VALID_USER, "wrong_password")

    assert login.is_error_visible()
    assert "Username and password do not match" in login.get_error_message()


@pytest.mark.e2e
def test_locked_user_cannot_login(page: Page):
    login = LoginPage(page)
    login.open().login("locked_out_user", VALID_PASSWORD)

    assert login.is_error_visible()
    assert "locked out" in login.get_error_message().lower()


@pytest.mark.e2e
def test_login_with_empty_credentials_shows_error(page: Page):
    login = LoginPage(page)
    login.open().login("", "")

    assert login.is_error_visible()
    assert "Username is required" in login.get_error_message()


@pytest.mark.e2e
def test_login_with_empty_password_shows_error(page: Page):
    login = LoginPage(page)
    login.open().login(VALID_USER, "")

    assert login.is_error_visible()
    assert "Password is required" in login.get_error_message()
