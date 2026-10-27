
from selenium.webdriver.common.by import By


def test_checkboxes_page(driver):
    driver.get("https://the-internet.herokuapp.com/checkboxes")

    checkboxes = driver.find_elements(
        By.CSS_SELECTOR, "input[type='checkbox']"
    )

    assert len(checkboxes) == 2


def test_dropdown_page(driver):
    driver.get("https://the-internet.herokuapp.com/dropdown")

    dropdown = driver.find_element(By.ID, "dropdown")
    options = dropdown.find_elements(By.TAG_NAME, "option")

    assert dropdown.is_displayed()
    assert len(options) == 3
