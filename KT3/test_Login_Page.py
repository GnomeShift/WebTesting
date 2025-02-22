from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import pytest
from Base_Page import BasePage


class AuthPage(BasePage):
    FIRSTNAME_FIELD = (By.XPATH, "//input[@name='firstname']")
    LASTNAME_FIELD = (By.XPATH, "//input[@name='lastname']")
    EMAIL_FIELD = (By.XPATH, "//*[@id='input-email']")
    PASSWORD_FIELD = (By.XPATH, "//*[@id='input-password']")
    LOGIN_BUTTON = (By.XPATH, "//*[@id='form-login']/div[3]/button")
    CONTINUE_BUTTON = (By.XPATH, "//button[text()='Continue']")
    AGREE_BUTTON = (By.XPATH, "//input[@name='agree']")
    PASSWORD_ERROR = (By.XPATH, "//div[text()='Password must be between 4 and 20 characters!']")

    MY_ACCOUNT_LINK = (By.XPATH, "//span[text()='My Account']")
    REGISTER_LINK = (By.XPATH, "//a[text()='Register']")
    LOGIN_LINK = (By.XPATH, "//a[text()='Login']")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def enter_firstname(self, firstname):
        self.driver.find_element(*self.FIRSTNAME_FIELD).send_keys(firstname)

    def enter_lastname(self, lastname):
        self.driver.find_element(*self.LASTNAME_FIELD).send_keys(lastname)

    def enter_email(self, email):
        self.driver.find_element(*self.EMAIL_FIELD).send_keys(email)

    def enter_password(self, password):
        self.driver.find_element(*self.PASSWORD_FIELD).send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def click_agree(self):
        self.driver.find_element(*self.AGREE_BUTTON).send_keys(Keys.SPACE)

    def click_continue(self):
        self.driver.find_element(*self.CONTINUE_BUTTON).click()

    def get_password_error_message(self):
        return self.driver.find_element(*self.PASSWORD_ERROR).text

    def get_account_header(self):
        return self.driver.find_element(By.XPATH, "//*[@id=\"content\"]/h2[1]")

    def get_signup_header(self):
        return self.driver.find_element(By.XPATH, "//*[@id='content']/h1")

    def open_login_page(self):
        self.driver.find_element(*self.MY_ACCOUNT_LINK).click()
        self.driver.find_element(*self.LOGIN_LINK).click()

    def open_register_page(self):
        self.driver.find_element(*self.MY_ACCOUNT_LINK).click()
        self.driver.find_element(*self.REGISTER_LINK).click()


class TestAuth:
    @pytest.fixture(scope="session")
    def auth_page(self, driver):
        return AuthPage(driver)

    def test_signup(self, auth_page):
        auth_page.open_register_page()

        first_name = "Test"
        last_name = "Test"
        email = "123@example.com"
        password = "123123"

        auth_page.enter_firstname(first_name)
        auth_page.enter_lastname(last_name)
        auth_page.enter_email(email)
        auth_page.enter_password(password)
        auth_page.click_agree()
        auth_page.click_continue()

        actual = auth_page.get_signup_header()
        assert actual.is_displayed()

    def test_signup_negative(self, auth_page):
        auth_page.open_register_page()

        first_name = "Test"
        last_name = "Test"
        email = "123@example.com"
        password = ""

        auth_page.enter_firstname(first_name)
        auth_page.enter_lastname(last_name)
        auth_page.enter_email(email)
        auth_page.enter_password(password)
        auth_page.click_agree()
        auth_page.click_continue()

        expected = "Password must be between 4 and 20 characters!"
        actual = auth_page.get_password_error_message()
        assert actual == expected

    def test_login(self, auth_page):
        auth_page.open_login_page()

        # Вводим данные
        auth_page.enter_email("123@example.com")
        auth_page.enter_password("123123")

        auth_page.click_login()
        actual = auth_page.get_account_header()
        assert actual.is_displayed()

@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Firefox()
    driver.maximize_window()
    yield driver
    driver.quit()
