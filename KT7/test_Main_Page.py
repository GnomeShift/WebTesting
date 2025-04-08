from Base_Page import BasePage
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException
from selenium import webdriver
import pytest
import json
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions


class MainPage(BasePage):
    FEATURED_PRODUCT = (By.CSS_SELECTOR, "#content > div.row .product-thumb")
    PRODUCT_NAME = (By.CSS_SELECTOR, ".description h4 a")
    PRODUCT_PRICE = (By.CSS_SELECTOR, ".description > .price span")
    CAROUSEL_ITEM = (By.CSS_SELECTOR, "#carousel-banner-0")
    HEADER = (By.CSS_SELECTOR, "#top")
    MONEY_LIST = (By.CSS_SELECTOR, "#top > div.row .product-thumb")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "#search button")
    SEARCH_FIELD = (By.XPATH, "//input[@name='search']")
    SEARCH_ICON = (By.XPATH, "//i[@class='fa-solid fa-magnifying-glass']")
    SEARCH_RESULT_HEADER = (By.XPATH, "//*[@id='content']/h1")
    MACBOOK_IMAGE_LINK = (By.XPATH, "//img[@title='MacBook']")
    MACBOOK_INVALID_IMAGE_LINK = (By.XPATH, "//img[@title='MacBook Pro Max']")
    IMAGE_COUNTER = (By.XPATH, "//div[text()='2 of 5']")
    POPUP_CLOSE_BUTTON = (By.XPATH, "/html/body/div[2]/div/button[2]")
    CURRENCY_DROPDOWN = (By.CLASS_NAME, "dropdown-toggle")
    EUR_CURRENCY_LINK = (By.XPATH, "//a[@href='EUR']")
    CURRENCY_SYMBOL = (By.XPATH, "//strong")
    DESKTOPS_LINK = (By.XPATH, f"//a[@href='{BasePage.BASE_URL}/en-gb/catalog/desktops']")
    PC_LINK = (By.XPATH, f"//a[@href='{BasePage.BASE_URL}/en-gb/catalog/desktops/pc']")
    CONTENT_TEXT = (By.ID, "content")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def open_main_page(self):
        self.driver.get(self.BASE_URL)

    def enter_search_text(self, text):
        self.driver.find_element(*self.SEARCH_FIELD).send_keys(text)

    def click_search_button(self):
        self.driver.find_element(*self.SEARCH_ICON).click()

    def get_search_result_header_text(self):
        return self.driver.find_element(*self.SEARCH_RESULT_HEADER).text

    def open_macbook_page(self):
        self.driver.get(f"{self.BASE_URL}/en-gb/product/macbook")

    def click_macbook_image(self):
        self.driver.find_element(*self.MACBOOK_IMAGE_LINK).click()

    def click_invalid_macbook_image(self):
        self.driver.find_element(*self.MACBOOK_INVALID_IMAGE_LINK).click()

    def close_popup(self):
        self.driver.find_element(*self.POPUP_CLOSE_BUTTON).click()

    def get_image_counter_text(self):
        return self.driver.find_element(*self.IMAGE_COUNTER).text

    def switch_to_eur_currency(self):
        self.driver.find_element(*self.CURRENCY_DROPDOWN).click()
        self.driver.find_element(*self.EUR_CURRENCY_LINK).click()

    def get_currency_symbol_text(self):
        return self.driver.find_element(*self.CURRENCY_SYMBOL).text

    def navigate_to_pc_page(self):
        self.driver.find_element(*self.DESKTOPS_LINK).click()
        self.driver.find_element(*self.PC_LINK).click()

    def get_content_text(self):
        return self.driver.find_element(*self.CONTENT_TEXT).text


class TestMainPage:
    @pytest.fixture(scope="session")
    def main_page(self, driver):
        return MainPage(driver)

    @pytest.mark.parametrize("search_text", ["MacBook", "iPhone"])
    def test_search(self, main_page, search_text):
        main_page.open_main_page()
        main_page.enter_search_text(search_text)
        main_page.click_search_button()

        expected = f"Search - {search_text}"
        actual = main_page.get_search_result_header_text()
        assert actual == expected
        main_page.screenshot("test_search.png")

    @pytest.mark.parametrize("search_text", ["Invalid Product Name"])
    def test_search_negative(self, main_page, search_text):
        main_page.open_main_page()
        main_page.enter_search_text(search_text)
        main_page.click_search_button()

        expected = f"Search - MacBook"
        actual = main_page.get_search_result_header_text()
        assert actual != expected
        main_page.screenshot("test_search_negative.png")

    def test_switch_screens(self, main_page):
        main_page.open_macbook_page()
        main_page.click_macbook_image()
        main_page.close_popup()

        expected = "2 of 5"
        actual = main_page.get_image_counter_text()
        assert actual == expected
        main_page.screenshot("test_switch_screens.png")

    def test_switch_screens_negative(self, main_page):
        main_page.open_macbook_page()
        try:
            main_page.click_invalid_macbook_image()
        except NoSuchElementException:
            assert True
            main_page.screenshot("test_search_negative.png")
        else:
            assert False, "NoSuchElementException не выдано"

    def test_switch_currency(self, main_page):
        main_page.open_main_page()
        main_page.switch_to_eur_currency()

        expected = "€"
        actual = main_page.get_currency_symbol_text()
        assert actual == expected
        main_page.screenshot("test_switch_currency.png")

    def test_switch_currency_negative(self, main_page):
        main_page.open_main_page()
        main_page.switch_to_eur_currency()

        expected = "$"
        actual = main_page.get_currency_symbol_text()
        assert actual != expected
        main_page.screenshot("test_switch_currency_negative.png")

    def test_page_pc(self, main_page):
        main_page.open_main_page()
        main_page.navigate_to_pc_page()

        expected = ("Desktops\n"
                    "Example of category description text\n"
                    "There are no products to list in this category.\n"
                    "Continue")
        actual = main_page.get_content_text()
        assert actual == expected
        main_page.screenshot("test_page_pc.png")

    def test_page_pc_negative(self, main_page):
        main_page.open_main_page()
        main_page.navigate_to_pc_page()

        expected = "There are nothing."
        actual = main_page.get_content_text()
        assert actual != expected
        main_page.screenshot("test_page_pc_negative.png")


@pytest.fixture(scope="session")
def driver(request):
    config_path = "params.json"

    with open(config_path, 'r') as f:
        config = json.load(f)

    browser_name = config.get("browserName", "firefox").lower()
    browser_version = config.get("browserVersion")
    selenoid_options = config.get("selenoid:options", {})

    if browser_name == "chrome":
        options = ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    elif browser_name == "firefox":
        options = FirefoxOptions()
        firefox_config = config.get("moz:firefoxOptions", {})
        if firefox_config:
            for pref_name, pref_value in firefox_config.get("prefs", {}).items():
                options.set_preference(pref_name, pref_value)
    else:
        raise ValueError(f"Неподдерживаемый браузер: {browser_name}")
    if browser_version:
        options.browser_version = browser_version

    options.set_capability("selenoid:options", selenoid_options)
    driver = webdriver.Remote(command_executor=BasePage.SELENOID_URL, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()
