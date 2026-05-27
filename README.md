# Playwright Python — Automation Testing Portfolio

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)
![Playwright](https://img.shields.io/badge/Playwright-1.40%2B-45ba4b?logo=playwright)
![pytest](https://img.shields.io/badge/pytest-7.4%2B-0a9edc)
![CI](https://github.com/rabinabdian/automation-playwright-python-solutions/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue)

A professional automation testing portfolio demonstrating real-world skills with **Playwright** and **Python** across UI, API, and data-driven testing patterns.

---

## Capabilities Demonstrated

| Skill | Where |
|---|---|
| **Page Object Model (POM)** | `pages/` — base class, locator encapsulation, method chaining |
| **Fixtures & dependency injection** | `conftest.py` — session/function scopes, shared auth state |
| **API testing** | `tests/api/` — Playwright's `APIRequestContext`, full CRUD coverage |
| **Data-driven / parametrize** | `tests/data_driven/` — `@pytest.mark.parametrize` with multiple datasets |
| **Custom markers** | `smoke`, `e2e`, `api`, `data_driven`, `regression` |
| **Screenshot on failure** | Auto-captured via `--screenshot=only-on-failure` |
| **Video recording** | Retained on failure via `--video=retain-on-failure` |
| **Trace viewer** | Full trace capture via `--tracing=retain-on-failure` |
| **Parallel execution** | `pytest-xdist` with `-n auto` |
| **HTML reporting** | `pytest-html` self-contained report at `reports/report.html` |
| **CI/CD pipeline** | GitHub Actions with artifact upload |

---

## Project Structure

```
.
├── conftest.py                     # Global fixtures (browser, auth, API context)
├── pyproject.toml                  # Dependencies + pytest config
├── pages/                          # Page Object Model layer
│   ├── base_page.py                # Base class: navigation, shared helpers
│   ├── login_page.py               # SauceDemo login interactions
│   ├── products_page.py            # Product listing + cart actions
│   ├── cart_page.py                # Shopping cart operations
│   └── checkout_page.py           # Multi-step checkout flow
├── tests/
│   ├── e2e/                        # End-to-end browser tests
│   │   ├── test_login.py           # Auth flows (valid, locked, empty)
│   │   ├── test_shopping_cart.py   # Cart add/remove/badge
│   │   └── test_checkout_flow.py  # Full purchase E2E + validation errors
│   ├── api/                        # API tests via Playwright request context
│   │   └── test_posts_api.py       # CRUD + filter + 404 against JSONPlaceholder
│   └── data_driven/                # Parametrized tests
│       └── test_parametrize.py     # User types, invalid credentials, sort options
├── utils/
│   └── helpers.py                  # retry(), scroll helpers, test data factory
└── .github/workflows/ci.yml        # GitHub Actions — smoke → E2E → API → reports
```

---

## Test Targets

| Target | Purpose |
|---|---|
| [saucedemo.com](https://www.saucedemo.com) | UI / E2E — login, cart, multi-step checkout |
| [jsonplaceholder.typicode.com](https://jsonplaceholder.typicode.com) | API — REST CRUD, filtering, error codes |

---

## Quick Start

```bash
# Clone and install
git clone https://github.com/rabinabdian/automation-playwright-python-solutions.git
cd automation-playwright-python-solutions
pip install -e .
playwright install chromium

# Run all tests (with HTML report)
pytest

# Run only smoke tests in parallel
pytest -m smoke -n auto

# Run a specific suite
pytest tests/e2e/
pytest tests/api/
pytest tests/data_driven/

# Run against multiple browsers
pytest tests/e2e/ --browser=chromium --browser=firefox --browser=webkit

# Open the HTML report
open reports/report.html        # macOS
xdg-open reports/report.html   # Linux
```

---

## Viewing Playwright Artifacts

When a test fails, Playwright captures a **screenshot**, **video**, and **trace** automatically.

```bash
# Open the trace viewer for a failed test
playwright show-trace test-results/<test-name>/trace.zip
```

---

## CI/CD

Every push triggers the GitHub Actions pipeline:

1. Install dependencies + Playwright browsers
2. Run **smoke** tests (fast gate)
3. Run **E2E**, **API**, and **data-driven** suites
4. Upload `reports/` as a build artifact (retained 30 days)

---

## Key Design Patterns

### Page Object Model with method chaining

```python
# tests are readable, pages are reusable
LoginPage(page).open().login("standard_user", "secret_sauce")
ProductsPage(page).add_product_to_cart("Sauce Labs Backpack").go_to_cart()
```

### Shared auth fixture (no repeated logins)

```python
# conftest.py
@pytest.fixture
def logged_in_page(page: Page) -> Page:
    LoginPage(page).open().login(STANDARD_USER, PASSWORD)
    page.wait_for_url("**/inventory.html")
    return page
```

### Data-driven parametrize

```python
@pytest.mark.parametrize("username,should_succeed,error_fragment", USER_LOGIN_SCENARIOS)
def test_login_scenarios(page, username, should_succeed, error_fragment):
    ...
```

### API testing with Playwright (no extra HTTP library needed)

```python
def test_create_post_returns_201(api_context: APIRequestContext):
    response = api_context.post("/posts", data={"title": "Test", "userId": 1})
    assert response.status == 201
```
