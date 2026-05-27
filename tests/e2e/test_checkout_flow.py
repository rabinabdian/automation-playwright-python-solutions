import pytest
from playwright.sync_api import Page

from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.helpers import checkout_info

SAUCE_LABS_BACKPACK = "Sauce Labs Backpack"


@pytest.mark.e2e
@pytest.mark.smoke
def test_full_checkout_flow_completes_successfully(logged_in_page: Page):
    info = checkout_info()

    ProductsPage(logged_in_page).add_product_to_cart(SAUCE_LABS_BACKPACK).go_to_cart()
    CartPage(logged_in_page).proceed_to_checkout()

    checkout = CheckoutPage(logged_in_page)
    checkout.fill_customer_info(info["first_name"], info["last_name"], info["postal_code"])
    checkout.continue_to_overview()

    assert "$" in checkout.get_total()

    checkout.finish_order()

    assert checkout.is_order_confirmed()
    assert "Thank you" in checkout.get_confirmation_message()


@pytest.mark.e2e
def test_checkout_without_first_name_shows_error(logged_in_page: Page):
    ProductsPage(logged_in_page).add_product_to_cart(SAUCE_LABS_BACKPACK).go_to_cart()
    CartPage(logged_in_page).proceed_to_checkout()

    checkout = CheckoutPage(logged_in_page)
    checkout.fill_customer_info("", "User", "12345")
    checkout.continue_to_overview()

    assert checkout.is_error_visible()


@pytest.mark.e2e
def test_checkout_without_postal_code_shows_error(logged_in_page: Page):
    ProductsPage(logged_in_page).add_product_to_cart(SAUCE_LABS_BACKPACK).go_to_cart()
    CartPage(logged_in_page).proceed_to_checkout()

    checkout = CheckoutPage(logged_in_page)
    checkout.fill_customer_info("Test", "User", "")
    checkout.continue_to_overview()

    assert checkout.is_error_visible()
