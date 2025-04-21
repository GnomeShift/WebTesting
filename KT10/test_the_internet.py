from Base_Page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common import (TimeoutException, NoSuchFrameException, StaleElementReferenceException,
                             NoSuchElementException)
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
import pytest
from time import sleep


class TheInternet(BasePage):
    AB_TEST_LINK = "https://the-internet.herokuapp.com/abtest"
    AB_TEST_HEADER = By.XPATH, "//*[@id=\"content\"]/div/h3"
    ADD_REMOVE_ELEMENTS_LINK = "https://the-internet.herokuapp.com/add_remove_elements/"
    ADD_REMOVE_ELEMENTS_ADD_ELEMENT_BUTTON = By.XPATH, "//*[@id=\"content\"]/div/button"
    ADD_REMOVE_ELEMENTS_DELETE_BUTTON = By.XPATH, "//*[@id=\"elements\"]/button"
    DISAPPEARED_ELEMENTS_LINK = "https://the-internet.herokuapp.com/disappearing_elements"
    DISAPPEARED_ELEMENTS_GALLERY_BUTTON = By.LINK_TEXT, "/gallery/"
    ENTRY_AD_LINK = "https://the-internet.herokuapp.com/entry_ad"
    ENTRY_AD_MODAL_HEADER = By.XPATH, "//div[contains(@class, \"modal-title\")]/h3"
    ENTRY_AD_CLOSE_BUTTON = By.XPATH, "//div[contains(@class, \"modal-footer\")]/p"
    LOGIN_LINK = "https://the-internet.herokuapp.com/login"
    LOGIN_USERNAME_FIELD = By.XPATH, "//input[@id=\"username\"]"
    LOGIN_PASSWORD_FIELD = By.XPATH, "//input[@id=\"password\"]"
    LOGIN_BUTTON = By.XPATH, "//button[contains(@class, \"radius\")]"
    LOGIN_ALERT = By.XPATH, "//div[@id=\"flash\"]"
    FORGOT_PASSWORD_LINK = "https://the-internet.herokuapp.com/forgot_password"
    FORGOT_PASSWORD_EMAIL_FIELD = By.XPATH, "//input[@id=\"email\"]"
    FORGOT_PASSWORD_BUTTON = By.XPATH, "//button[contains(@class, \"radius\")]"
    FORGOT_PASSWORD_ERROR_MESSAGE = By.XPATH, "/html/body/h1"
    KEY_PRESSES_LINK = "https://the-internet.herokuapp.com/key_presses?"
    KEY_PRESSES_INPUT = By.XPATH, "//input[@id=\"target\"]"
    KEY_PRESSES_RESULT = By.XPATH, "//p[@id=\"result\"]"
    NOTIFICATION_MESSAGE_LINK = "https://the-internet.herokuapp.com/notification_message_rendered"
    NOTIFICATION_MESSAGE_NEW_MESSAGE_LINK = By.XPATH, "//a[contains(text(), 'Click here')]"
    NOTIFICATION_MESSAGE_ALERT = By.XPATH, "//*[@id=\"flash\"]"
    REDIRECTION_LINK = "https://the-internet.herokuapp.com/redirector"
    REDIRECTION_BUTTON = By.XPATH, "//*[@id=\"redirect\"]"
    STATUS_CODE_LINK = "https://the-internet.herokuapp.com/status_codes"
    STATUS_CODE_200 = By.XPATH, "//a[contains(text(), '200')]"
    STATUS_CODE_DESCRIPTION = By.XPATH, "//div[@id=\"content\"]/div/p"

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def find_element(self, locator: tuple[str, str], frame_locator: tuple[str, str] = None, max_attempts=3):
        for attempt in range(max_attempts):
            try:
                if frame_locator:
                    try:
                        frame = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(frame_locator))
                        self.driver.switch_to.frame(frame)
                    except (TimeoutException, NoSuchFrameException) as e:
                        print(f"Ошибка при переключении на фрейм {frame_locator}: {e}")
                        pass
                element: WebElement = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator))
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(element))
                return element
            except (TimeoutException, StaleElementReferenceException) as e:
                print(f"Ошибка (попытка {attempt + 1}): {e}")
                pass
            finally:
                try:
                    if frame_locator:
                        self.driver.switch_to.default_content()
                except Exception as e:
                    print(f"Не удалось вернуться к основному контенту: {e}")
        print(f"Не удалось найти элемент после {max_attempts} попыток с локатором {locator}")

    def find_and_click_element(self, locator: tuple[str, str], frame_locator: tuple[str, str] = None, max_attempts=3):
        for attempt in range(max_attempts):
            try:
                if frame_locator:
                    try:
                        frame = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(frame_locator))
                        self.driver.switch_to.frame(frame)
                    except (TimeoutException, NoSuchFrameException) as e:
                        print(f"Ошибка при переключении на фрейм {frame_locator}: {e}")
                        pass
                element: WebElement = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(locator))
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(element))
                try:
                    self.driver.execute_script("arguments[0].click();", element)
                    return
                except StaleElementReferenceException as e:
                    print(f"StaleElementReferenceException при клике (попытка {attempt + 1}): {e}")
                    pass
            except (TimeoutException, StaleElementReferenceException) as e:
                print(f"Ошибка (попытка {attempt + 1}): {e}")
                pass
            finally:
                try:
                    if frame_locator:
                        self.driver.switch_to.default_content()
                except Exception as e:
                    print(f"Не удалось вернуться к основному контенту: {e}")
        print(f"Не удалось кликнуть на элемент после {max_attempts} попыток с локатором {locator}")

    def get_element_text(self, locator: tuple[str, str]):
        return self.driver.find_element(*locator).text

    def is_element_displayed(self, locator: tuple[str, str]):
        return self.driver.find_element(*locator).is_displayed()

    def enter_login_pass(self, username, password):
        self.driver.find_element(*self.LOGIN_USERNAME_FIELD).send_keys(username)
        self.driver.find_element(*self.LOGIN_PASSWORD_FIELD).send_keys(password)

    def enter_text(self, locator: tuple[str, str], text):
        self.driver.find_element(*locator).send_keys(text)


class TestTheInternet:
    @pytest.fixture(scope="session")
    def the_internet(self, driver):
        return TheInternet(driver)

    def test_ab(self, the_internet, driver):
        driver.get(the_internet.AB_TEST_LINK)
        header = the_internet.get_element_text(the_internet.AB_TEST_HEADER)
        assert header == "A/B Test Control" or header == "A/B Test Variation 1"

    def test_add_remove_elements(self, the_internet, driver):
        driver.get(the_internet.ADD_REMOVE_ELEMENTS_LINK)
        the_internet.find_and_click_element(the_internet.ADD_REMOVE_ELEMENTS_ADD_ELEMENT_BUTTON)
        assert the_internet.is_element_displayed(the_internet.ADD_REMOVE_ELEMENTS_DELETE_BUTTON)

    def test_disappearing_elements(self, the_internet, driver):
        driver.get(the_internet.DISAPPEARED_ELEMENTS_LINK)
        try:
            if the_internet.is_element_displayed(the_internet.DISAPPEARED_ELEMENTS_GALLERY_BUTTON):
                assert True
        except NoSuchElementException:
            assert True

    def test_entry_ad(self, the_internet, driver):
        driver.get(the_internet.ENTRY_AD_LINK)
        sleep(1)
        header_text = the_internet.get_element_text(the_internet.ENTRY_AD_MODAL_HEADER)
        if header_text == "THIS IS A MODAL WINDOW":
            the_internet.find_and_click_element(the_internet.ENTRY_AD_CLOSE_BUTTON)
            sleep(0.5)
            if not the_internet.is_element_displayed(the_internet.ENTRY_AD_MODAL_HEADER):
                assert True
        else:
            print(f"Текст заголовка: {header_text}")
            assert False

    @pytest.mark.parametrize("username", ["tomsmith"])
    @pytest.mark.parametrize("password", ["SuperSecretPassword!"])
    def test_login(self, the_internet, driver, username, password):
        driver.get(the_internet.LOGIN_LINK)
        the_internet.enter_login_pass(username, password)
        the_internet.find_and_click_element(the_internet.LOGIN_BUTTON)
        sleep(1)
        alert_text = the_internet.get_element_text(the_internet.LOGIN_ALERT)
        assert alert_text == "You logged into a secure area!\n×"

    @pytest.mark.parametrize("email", ["123@example.com"])
    def test_forgot_password(self, the_internet, driver, email):
        driver.get(the_internet.FORGOT_PASSWORD_LINK)
        the_internet.enter_text(the_internet.FORGOT_PASSWORD_EMAIL_FIELD, email)
        the_internet.find_and_click_element(the_internet.FORGOT_PASSWORD_BUTTON)
        message_text = the_internet.get_element_text(the_internet.FORGOT_PASSWORD_ERROR_MESSAGE)
        assert message_text == "Internal Server Error"

    def test_key_presses(self, the_internet, driver):
        driver.get(the_internet.KEY_PRESSES_LINK)
        the_internet.enter_text(the_internet.KEY_PRESSES_INPUT, Keys.SHIFT)
        result_text = the_internet.get_element_text(the_internet.KEY_PRESSES_RESULT)
        assert result_text == "You entered: SHIFT"

    def test_notification_message(self, the_internet, driver):
        driver.get(the_internet.NOTIFICATION_MESSAGE_LINK)
        driver.find_element(*the_internet.NOTIFICATION_MESSAGE_NEW_MESSAGE_LINK).click()
        alert_text = the_internet.get_element_text(the_internet.NOTIFICATION_MESSAGE_ALERT)
        print(f"Текст: {alert_text}")
        assert alert_text == "Action successful\n×" or alert_text == "Action unsuccesful, please try again\n×"

    def test_redirection(self, the_internet, driver):
        driver.get(the_internet.REDIRECTION_LINK)
        base_url = "https://the-internet.herokuapp.com/redirector"
        the_internet.find_and_click_element(the_internet.REDIRECTION_BUTTON)
        sleep(1)
        actual_url = driver.current_url
        assert actual_url != base_url

    def test_status_code(self, the_internet, driver):
        driver.get(the_internet.STATUS_CODE_LINK)
        the_internet.find_and_click_element(the_internet.STATUS_CODE_200)
        sleep(1)
        description = the_internet.get_element_text(the_internet.STATUS_CODE_DESCRIPTION)
        assert description == "This page returned a 200 status code.\n\nFor a definition and common list of HTTP status codes, go here"


@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Firefox()
    driver.maximize_window()
    yield driver
    driver.quit()
