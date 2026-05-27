from playwright.sync_api import Page
from pages.base_page import BasePage


class CartPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.cart_items = page.locator(".cart_item")
        self.checkout_button = page.locator("[data-test='checkout']")
        self.continue_shopping_button = page.locator("[data-test='continue-shopping']")

    def get_item_count(self) -> int:
        return self.cart_items.count()

    def get_item_names(self) -> list[str]:
        return self.page.locator(".inventory_item_name").all_text_contents()

    def proceed_to_checkout(self) -> "CartPage":
        self.checkout_button.click()
        return self

    def continue_shopping(self) -> "CartPage":
        self.continue_shopping_button.click()
        return self

    def remove_item(self, item_name: str) -> "CartPage":
        self.page.locator(f".cart_item:has-text('{item_name}')").locator("button").click()
        return self
