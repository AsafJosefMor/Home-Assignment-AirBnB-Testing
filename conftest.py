import pytest
from pathlib import Path

# Override Playwright's default context fixture
@pytest.fixture(scope="function")
def context(browser):
    # Always use a "maximized" viewport, safe even in headless
    return browser.new_context(viewport={"width": 2560, "height": 1440})

# Reuse the existing page fixture from pytest-playwright
@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page
    context.close()

# Take browser UI screenshot on failure (Called automatically by pytest on failure)
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Get the outcome of the test
    outcome = yield
    report = outcome.get_result()

    # Only act on failures during the "call" phase (not setup/teardown)
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page", None)

        if page:
            reports_dir = Path("reports")
            reports_dir.mkdir(exist_ok=True)
            test_name = item.name.replace("/", "_").replace("\\", "_")

            # Screenshot on failure
            screenshot_path = reports_dir / Path("screenshots") / f"{test_name}.png"
            page.screenshot(path=screenshot_path)

            # Log in terminal
            print(f"\n[Screenshot saved to {screenshot_path}]")