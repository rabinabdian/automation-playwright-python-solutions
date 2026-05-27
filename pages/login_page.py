from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator("[data-test='error']")

    def open(self) -> "LoginPage":
        self.navigate("/")
        return self

    def login(self, username: str, password: str) -> "LoginPage":
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        return self

    def get_error_message(self) -> str:
        return self.error_message.text_content() or ""

    def is_error_visible(self) -> bool:
        return self.error_message.is_visible()
