from playwright.sync_api import Page, expect


class BasePage:
    BASE_URL = "https://www.saucedemo.com"

    def __init__(self, page: Page):
        self.page = page

    def navigate(self, path: str = ""):
        self.page.goto(f"{self.BASE_URL}{path}")

    def get_title(self) -> str:
        return self.page.title()

    def wait_for_url_contains(self, path: str):
        self.page.wait_for_url(f"**{path}**")
