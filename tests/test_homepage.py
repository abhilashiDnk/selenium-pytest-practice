
from selenium.webdriver.common.by import By


def test_homepage_loads(driver):
    driver.get("https://the-internet.herokuapp.com/")

    assert driver.title == "The Internet"

    heading = driver.find_element(By.TAG_NAME, "h1")
    assert heading.is_displayed()
    assert heading.text == "Welcome to the-internet"
