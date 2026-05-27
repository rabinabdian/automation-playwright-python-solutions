import pytest
from playwright.sync_api import Page, expect

from pages.products_page import ProductsPage
from pages.cart_page import CartPage

SAUCE_LABS_BACKPACK = "Sauce Labs Backpack"
SAUCE_LABS_BIKE_LIGHT = "Sauce Labs Bike Light"


@pytest.mark.e2e
@pytest.mark.smoke
def test_add_single_item_updates_cart_badge(logged_in_page: Page):
    products = ProductsPage(logged_in_page)
    assert products.get_cart_count() == 0

    products.add_product_to_cart(SAUCE_LABS_BACKPACK)

    assert products.get_cart_count() == 1


@pytest.mark.e2e
def test_add_multiple_items_reflects_correct_count(logged_in_page: Page):
    products = ProductsPage(logged_in_page)

    products.add_product_to_cart(SAUCE_LABS_BACKPACK)
    products.add_product_to_cart(SAUCE_LABS_BIKE_LIGHT)

    assert products.get_cart_count() == 2


@pytest.mark.e2e
def test_added_item_appears_in_cart(logged_in_page: Page):
    products = ProductsPage(logged_in_page)
    products.add_product_to_cart(SAUCE_LABS_BACKPACK)
    products.go_to_cart()

    cart = CartPage(logged_in_page)
    assert cart.get_item_count() == 1
    assert SAUCE_LABS_BACKPACK in cart.get_item_names()


@pytest.mark.e2e
def test_remove_item_from_cart(logged_in_page: Page):
    products = ProductsPage(logged_in_page)
    products.add_product_to_cart(SAUCE_LABS_BACKPACK)
    products.go_to_cart()

    cart = CartPage(logged_in_page)
    assert cart.get_item_count() == 1

    cart.remove_item(SAUCE_LABS_BACKPACK)

    assert cart.get_item_count() == 0


@pytest.mark.e2e
def test_continue_shopping_returns_to_products(logged_in_page: Page):
    products = ProductsPage(logged_in_page)
    products.go_to_cart()

    cart = CartPage(logged_in_page)
    cart.continue_shopping()

    expect(logged_in_page).to_have_url("https://www.saucedemo.com/inventory.html")
