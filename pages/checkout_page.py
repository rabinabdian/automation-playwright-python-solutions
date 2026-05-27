from playwright.sync_api import Page
from pages.base_page import BasePage


class CheckoutPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name_input = page.locator("[data-test='firstName']")
        self.last_name_input = page.locator("[data-test='lastName']")
        self.postal_code_input = page.locator("[data-test='postalCode']")
        self.continue_button = page.locator("[data-test='continue']")
        self.finish_button = page.locator("[data-test='finish']")
        self.error_message = page.locator("[data-test='error']")
        self.summary_total = page.locator(".summary_total_label")
        self.confirmation_header = page.locator(".complete-header")
        self.back_home_button = page.locator("[data-test='back-to-products']")

    def fill_customer_info(self, first_name: str, last_name: str, postal_code: str) -> "CheckoutPage":
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        return self

    def continue_to_overview(self) -> "CheckoutPage":
        self.continue_button.click()
        return self

    def finish_order(self) -> "CheckoutPage":
        self.finish_button.click()
        return self

    def get_total(self) -> str:
        return self.summary_total.text_content() or ""

    def is_order_confirmed(self) -> bool:
        return self.confirmation_header.is_visible()

    def get_confirmation_message(self) -> str:
        return self.confirmation_header.text_content() or ""

    def is_error_visible(self) -> bool:
        return self.error_message.is_visible()
