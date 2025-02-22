from selenium.webdriver.remote.webelement import WebElement
from selenium.common import StaleElementReferenceException, NoSuchFrameException
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import pytest
from Base_Page import BasePage


class ProductPage(BasePage):
    PHONES_PAGE_LINK = (By.XPATH, "//*[@id=\"narbar-menu\"]/ul/li[6]/a")
    CAMERAS_PAGE_LINK = (By.XPATH, "//*[@id=\"narbar-menu\"]/ul/li[7]/a")
    TABLETS_PAGE_LINK = (By.XPATH, "//*[@id=\"narbar-menu\"]/ul/li[4]/a")

    WISHLIST_ON_PRODUCT_PAGE_BUTTON = (By.XPATH, "//*[@id=\"content\"]/div[1]/div[2]/form/div/button[1]")
    PRODUCT_NAME = (By.XPATH, "//*[@id=\"content\"]/div[2]/div/div/div[1]/a/img")

    OPTIONAL_SUBMENU = (By.XPATH, "//*[@id=\"input-option-226\"]")
    RED_COLOR = (By.XPATH, "//*[@id=\"input-option-226\"]/option[2]")
    ADD_TO_CART_BUTTON = (By.XPATH, "//*[@id=\"button-cart\"]")

    REVIEWS_BUTTON = (By.XPATH, "//*[@id=\"content\"]/ul/li[3]/a")
    CONTINUE_REVIEW_BUTTON = (By.XPATH, "//*[@id=\"button-review\"]")
    REVIEW_NAME_FIELD = (By.XPATH, "//*[@id=\"input-name\"]")
    REVIEW_TEXT = (By.XPATH, "//*[@id=\"input-text\"]")
    REVIEW_RATING = (By.XPATH, "//*[@id=\"input-rating\"]")

    LOGIN_ALERT = (By.XPATH, "//*[@id=\"alert\"]/div")
    CART_ALERT = (By.XPATH, "//*[@id=\"alert\"]/div")

    def __init__(self, driver):
        super().__init__(driver)

    def open_main_page(self):
        self.driver.get(self.BASE_URL)

    def click_product_name(self, product_index, frame_locator=None, max_attempts=3):
        for attempt in range(max_attempts):
            try:
                if frame_locator:
                    try:
                        frame = WebDriverWait(self.driver, 3).until(
                            EC.presence_of_element_located(frame_locator))
                        self.driver.switch_to.frame(frame)
                    except (TimeoutException, NoSuchFrameException) as e:
                        print(f"Ошибка при переключении на фрейм {frame_locator}: {e}")
                        pass

                products = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located(self.PRODUCT_NAME))
                element = products[product_index]
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(element))

                try:
                    element.click()
                    return
                except StaleElementReferenceException as e:
                    print(f"StaleElementReferenceException при клике (попытка {attempt + 1}): {e}")
                    pass

            except (TimeoutException, StaleElementReferenceException) as e:
                print(f"Ошибка (попытка {attempt + 1}): {e}")
                pass
            finally:
                try:
                    self.driver.switch_to.default_content()
                except Exception as e:
                    print(f"Не удалось вернуться к основному контенту: {e}")

        print(f"Не удалось кликнуть на элемент с индексом {product_index} после {max_attempts} попыток")

    def find_and_click_element(self, locator: tuple[str, str], frame_locator: tuple[str, str] = None, max_attempts=3):
        for attempt in range(max_attempts):
            try:
                if frame_locator:
                    try:
                        frame = WebDriverWait(self.driver, 3).until(
                            EC.presence_of_element_located(frame_locator))
                        self.driver.switch_to.frame(frame)
                    except (TimeoutException, NoSuchFrameException) as e:
                        print(f"Ошибка при переключении на фрейм {frame_locator}: {e}")
                        pass

                element: WebElement = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(locator))

                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(element))

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

    def open_phones_page(self):
        self.driver.find_element(*self.PHONES_PAGE_LINK).click()

    def open_cameras_page(self):
        self.driver.find_element(*self.CAMERAS_PAGE_LINK).click()

    def open_optional_options(self):
        self.driver.find_element(*self.OPTIONAL_SUBMENU).click()

    def open_tablets_page(self):
        self.driver.find_element(*self.TABLETS_PAGE_LINK).click()

    def select_red_color(self):
        self.driver.find_element(*self.RED_COLOR).click()

    def get_login_alert_text(self):
        return self.driver.find_element(*self.LOGIN_ALERT).text

    def is_login_alert_displayed(self):
        try:
            self.driver.find_element(*self.LOGIN_ALERT).is_displayed()
            return True
        except:
            return False

    def is_cart_alert_displayed(self):
        try:
            self.driver.find_element(*self.CART_ALERT).is_displayed()
            return True
        except:
            return False

    def is_this_cart_alert(self, expected):
        actual = self.driver.find_element(*self.CART_ALERT).get_attribute("textContent")

        if actual == expected:
            return True
        else:
            print("Текст уведомления не совпадает")
            return False

    def write_a_review(self, name, review_text):
        self.find_and_click_element(self.REVIEW_NAME_FIELD)
        name_field = self.driver.find_element(*self.REVIEW_NAME_FIELD)
        name_field.clear()
        name_field.send_keys(name)
        self.find_and_click_element(self.REVIEW_TEXT)
        text_field = self.driver.find_element(*self.REVIEW_TEXT)
        text_field.clear()
        text_field.send_keys(review_text)

    def rate_the_product(self, rating):
        buttons = self.driver.find_elements(*self.REVIEW_RATING)

        for button in buttons:
            if button.get_attribute("value") == str(rating):
                button.click()
                return
        print(f"Кнопка с рейтингом {rating} не найдена")

    def get_actual_reviewer_name(self):
        return self.driver.find_element(*self.REVIEW_NAME_FIELD).get_attribute("value")

    def get_actual_review_text(self):
        return self.driver.find_element(*self.REVIEW_TEXT).get_attribute("value")


class TestProductPage:
    @pytest.fixture(scope="session")
    def product_page(self, driver):
        return ProductPage(driver)

    @pytest.mark.parametrize("product_index", [0, 1, 2])
    def test_add_to_wishlist_from_main_page_logged_out(self, product_page, product_index):
        product_page.open_main_page()
        product_page.click_product_name(product_index)
        product_page.find_and_click_element(product_page.WISHLIST_ON_PRODUCT_PAGE_BUTTON)
        assert product_page.is_login_alert_displayed()

    @pytest.mark.parametrize("product_index", [0, 1, 2])
    def test_add_to_wishlist_from_product_page_logged_out(self, product_page, product_index):
        product_page.open_main_page()
        product_page.click_product_name(product_index)
        product_page.find_and_click_element(product_page.WISHLIST_ON_PRODUCT_PAGE_BUTTON)
        assert product_page.is_login_alert_displayed()

    @pytest.mark.parametrize("expected", [" Success: You have added Canon EOS 5D to your shopping cart! "])
    def test_add_camera_to_cart(self, product_page, expected):
        product_page.open_main_page()
        product_page.open_cameras_page()
        product_page.click_product_name(product_index=0)
        product_page.open_optional_options()
        product_page.select_red_color()
        product_page.find_and_click_element(product_page.ADD_TO_CART_BUTTON)

        if product_page.is_cart_alert_displayed():
            if product_page.is_this_cart_alert(expected):
                assert True
            else:
                print("Это уведомление не о добавлении в корзину")
                assert False
        else:
            print("Уведомление не появилось")
            assert False

    @pytest.mark.parametrize("expected", [" Success: You have added Samsung Galaxy Tab 10.1 to your shopping cart! "])
    def test_add_tabled_to_cart(self, product_page, expected):
        product_page.open_main_page()
        product_page.open_tablets_page()
        product_page.click_product_name(product_index=0)
        product_page.find_and_click_element(product_page.ADD_TO_CART_BUTTON)

        if product_page.is_cart_alert_displayed():
            if product_page.is_this_cart_alert(expected):
                assert True
            else:
                print("Это уведомление не о добавлении в корзину")
                assert False
        else:
            print("Уведомление не появилось")
            assert False

    @pytest.mark.parametrize("expected", [" Success: You have added HTC Touch HD to your shopping cart! "])
    def test_add_htc_phone_to_cart(self, product_page, expected):
        product_page.open_main_page()
        product_page.open_phones_page()
        product_page.click_product_name(product_index=0)
        product_page.find_and_click_element(product_page.ADD_TO_CART_BUTTON)

        if product_page.is_cart_alert_displayed():
            if product_page.is_this_cart_alert(expected):
                assert True
            else:
                print("Это уведомление не о добавлении в корзину")
                assert False
        else:
            print("Уведомление не появилось")
            assert False

    @pytest.mark.parametrize("product_index", [0])
    @pytest.mark.parametrize("name", ["Reviewer"])
    @pytest.mark.parametrize("review_text", ["I really like it!"])
    @pytest.mark.parametrize("rating", [5])
    def test_write_review(self, driver, product_page, product_index, name, review_text, rating):
        product_page.open_main_page()
        product_page.click_product_name(product_index)
        product_page.find_and_click_element(product_page.REVIEWS_BUTTON)
        product_page.write_a_review(name, review_text)
        product_page.rate_the_product(rating)
        product_page.find_and_click_element(product_page.CONTINUE_REVIEW_BUTTON)
        actual_reviewer_name = product_page.get_actual_reviewer_name()
        actual_review_text = product_page.get_actual_review_text()
        assert actual_reviewer_name == name and actual_review_text == review_text


@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Firefox()
    driver.maximize_window()
    yield driver
    driver.quit()
