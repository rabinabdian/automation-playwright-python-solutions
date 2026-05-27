import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.products_page import ProductsPage

PASSWORD = "secret_sauce"

# (username, should_login_succeed, expected_error_fragment)
USER_LOGIN_SCENARIOS = [
    ("standard_user", True, None),
    ("locked_out_user", False, "locked out"),
    ("problem_user", True, None),
    ("performance_glitch_user", True, None),
]

INVALID_CREDENTIAL_SCENARIOS = [
    ("standard_user", "wrongpass", "do not match"),
    ("no_such_user", PASSWORD, "do not match"),
    ("", "", "Username is required"),
    ("standard_user", "", "Password is required"),
]

# (sort_option, is_ascending, sort_by_price)
SORT_SCENARIOS = [
    ("az", True, False),
    ("za", False, False),
    ("lohi", True, True),
    ("hilo", False, True),
]


@pytest.mark.data_driven
@pytest.mark.parametrize("username,should_succeed,error_fragment", USER_LOGIN_SCENARIOS)
def test_login_scenarios(page: Page, username: str, should_succeed: bool, error_fragment):
    login = LoginPage(page)
    login.open().login(username, PASSWORD)

    if should_succeed:
        page.wait_for_url("**/inventory.html")
        assert "/inventory.html" in page.url
    else:
        assert login.is_error_visible()
        assert error_fragment in login.get_error_message().lower()


@pytest.mark.data_driven
@pytest.mark.parametrize("username,password,error_fragment", INVALID_CREDENTIAL_SCENARIOS)
def test_invalid_credential_combinations(page: Page, username: str, password: str, error_fragment: str):
    login = LoginPage(page)
    login.open().login(username, password)

    assert login.is_error_visible()
    assert error_fragment in login.get_error_message()


@pytest.mark.data_driven
@pytest.mark.parametrize("sort_option,ascending,by_price", SORT_SCENARIOS)
def test_product_sort_options(logged_in_page: Page, sort_option: str, ascending: bool, by_price: bool):
    products = ProductsPage(logged_in_page)
    products.sort_by(sort_option)

    if by_price:
        prices = products.get_product_prices()
        assert prices == sorted(prices, reverse=not ascending), (
            f"Prices not sorted correctly for option '{sort_option}': {prices}"
        )
    else:
        names = products.get_product_names()
        assert names == sorted(names, reverse=not ascending), (
            f"Names not sorted correctly for option '{sort_option}': {names}"
        )
