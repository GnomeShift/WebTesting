import pytest
from Base_Page import BasePage
from test_Product_Page import ProductPage
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions


class CartPage(BasePage):
    CART_PAGE_LINK = (By.XPATH, "//*[@id=\"top\"]/div/div[2]/ul/li[4]/a/span")
    CART_CONTENT = (By.XPATH, "//*[@id=\"content\"]")

    def __init__(self, driver):
        super().__init__(driver)

    @pytest.fixture(scope="session")
    def product_page(self, driver):
        return ProductPage(driver)

    def open_main_page(self):
        self.driver.get(BasePage.BASE_URL)

    def open_cart_page(self):
        self.driver.find_element(*self.CART_PAGE_LINK).click()

    def get_cart_content(self):
        return self.driver.find_element(*self.CART_CONTENT).text

    def add_htc_phone_to_cart(self, product_page):
        product_page.open_main_page()
        product_page.open_phones_page()
        product_page.click_product_name(product_index=0)
        product_page.find_and_click_element(product_page.ADD_TO_CART_BUTTON)


class TestCartPage:
    @pytest.fixture(scope="session")
    def cart_page(self, driver):
        return CartPage(driver)

    @pytest.fixture(scope="session")
    def product_page(self, driver):
        return ProductPage(driver)

    def test_empty_cart(self, cart_page):
        cart_page.open_main_page()
        cart_page.open_cart_page()
        cart_page.get_cart_content()
        assert cart_page.get_cart_content() == "Shopping Cart\nYour shopping cart is empty!\nContinue"
        cart_page.screenshot("test_empty_cart.png")

    def test_non_empty_cart(self, cart_page, product_page):
        cart_page.add_htc_phone_to_cart(product_page)
        cart_page.open_main_page()
        cart_page.open_cart_page()
        actual_cart_content = cart_page.get_cart_content()
        assert actual_cart_content == "Shopping Cart (0.15kg)\nImage Product Name Model Quantity Unit Price Total\nHTC Touch HD\n- Reward Points: 400 Product 1\n$122.00 $122.00\nSub-Total $100.00\nEco Tax (-2.00) $2.00\nVAT (20%) $20.00\nTotal $122.00\nWhat would you like to do next?\nChoose if you have a discount code or reward points you want to use or would like to estimate your delivery cost.\nEstimate Shipping & Taxes\nUse Coupon Code\nUse Gift Certificate\n\nContinue Shopping\nCheckout"
        cart_page.screenshot("test_non_empty_cart.png")


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
