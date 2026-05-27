from playwright.sync_api import Page
from pages.base_page import BasePage


class ProductsPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.product_items = page.locator(".inventory_item")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")
        self.sort_dropdown = page.locator("[data-test='product-sort-container']")
        self.page_title = page.locator(".title")

    def get_product_count(self) -> int:
        return self.product_items.count()

    def add_product_to_cart(self, product_name: str) -> "ProductsPage":
        self.page.locator(f".inventory_item:has-text('{product_name}')").locator("button").click()
        return self

    def add_first_product_to_cart(self) -> "ProductsPage":
        self.product_items.first.locator("button").click()
        return self

    def get_cart_count(self) -> int:
        if not self.cart_badge.is_visible():
            return 0
        return int(self.cart_badge.text_content() or "0")

    def go_to_cart(self) -> "ProductsPage":
        self.cart_link.click()
        return self

    def sort_by(self, option: str) -> "ProductsPage":
        """Options: 'az', 'za', 'lohi', 'hilo'"""
        self.sort_dropdown.select_option(option)
        return self

    def get_product_names(self) -> list[str]:
        return self.page.locator(".inventory_item_name").all_text_contents()

    def get_product_prices(self) -> list[float]:
        prices = self.page.locator(".inventory_item_price").all_text_contents()
        return [float(p.replace("$", "")) for p in prices]

    def is_loaded(self) -> bool:
        return self.page_title.is_visible() and self.page_title.text_content() == "Products"
