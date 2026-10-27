
import csv
from pathlib import Path

import pytest


@pytest.fixture
def driver():
    """Create a browser for a test and close it after the test."""
    from selenium import webdriver

    browser = webdriver.Edge()
    yield browser
    browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture the test result and take a screenshot on failure."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        browser = item.funcargs.get("driver")

        if browser is not None:
            screenshot_dir = Path("screenshots")
            screenshot_dir.mkdir(parents=True, exist_ok=True)

            screenshot_name = item.name.replace("/", "_") + ".png"
            screenshot_path = screenshot_dir / screenshot_name

            try:
                browser.save_screenshot(str(screenshot_path))
                print(f"\nFailure screenshot saved: {screenshot_path}")
            except Exception as error:
                print(f"\nCould not save screenshot: {error}")


def pytest_sessionfinish(session, exitstatus):
    """Export the pytest results to CSV."""
    report_dir = Path("reports")
    report_dir.mkdir(parents=True, exist_ok=True)

    csv_path = report_dir / "report.csv"

    terminal_report = session.config.pluginmanager.get_plugin(
        "terminalreporter"
    )

    if terminal_report is None:
        return

    results = []

    for outcome in ("passed", "failed", "skipped"):
        for report in terminal_report.stats.get(outcome, []):
            results.append({
                "Test": report.nodeid,
                "Result": outcome.upper(),
                "Duration (seconds)": round(report.duration, 2),
            })

    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "Test",
                "Result",
                "Duration (seconds)",
            ],
        )
        writer.writeheader()
        writer.writerows(results)

    print(f"\nCSV report saved to: {csv_path}")
