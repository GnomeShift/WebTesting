from Base_Page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common import (TimeoutException, NoSuchFrameException, StaleElementReferenceException,
                             NoSuchElementException)
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
import pytest
from time import sleep
from selenium.common import UnexpectedAlertPresentException


class AdminPage(BasePage):
    USERNAME_FIELD = By.XPATH, "//*[@id='input-username']"
    PASSWORD_FIELD = By.XPATH, "//*[@id='input-password']"
    LOGIN_BUTTON = By.XPATH, "//*[@id='form-login']/div[3]/button"
    USERNAME = "user"
    PASSWORD = "bitnami"
    CATALOG_MENU = By.XPATH, "//*[@id='menu-catalog']/a"
    CATEGORIES_SUBMENU = By.XPATH, "//*[@id='collapse-1']/li[1]/a"
    PRODUCTS_SUBMENU = By.XPATH, "//*[@id='collapse-1']/li[2]/a"
    ADD_BUTTON = By.XPATH, "//*[@id='content']//a[contains(@class, 'btn btn-primary') and @data-bs-original-title='Add New']"
    CATEGORY_NAME_FIELD = By.XPATH, "//*[@id='input-name-1']"
    PRODUCT_NAME_FIELD = By.XPATH, "//*[@id='input-name-1']"
    META_TAG_TITLE_FIELD = By.XPATH, "//*[@id='input-meta-title-1']"
    CATEGORIES_FIELD = By.XPATH, "//*[@id='input-category']"
    MODEL_FIELD = By.XPATH, "//*[@id='input-model']"
    PRODUCT_SEO_TAB = By.XPATH, "//*[@id='form-product']//a[text()='SEO']"
    CATEGORY_SEO_TAB = By.XPATH, "//*[@id='form-category']//a[text()='SEO']"
    PRODUCT_DATA_TAB = By.XPATH, "//*[@id='form-product']//a[text()='Data']"
    PRODUCT_LINKS_TAB = By.XPATH, "//*[@id='form-product']//a[text()='Links']"
    SEO_URL_FIELD = By.XPATH, "//*[@id='input-keyword-0-1']"
    MAIN_PAGE_LINK = By.XPATH, "//*[@id='header']/div/a/img"
    CATEGORIES_TABLE_SECOND_PAGE = By.XPATH, "//*[@id='form-category']/div[2]/div[1]/ul/li[2]/a"
    PRODUCTS_TABLE_SECOND_PAGE = By.XPATH, "//*[@id='form-product']/div[2]/div[1]/ul/li[2]/a"
    DEVICES_CATEGORY = By.XPATH, "//*[@id='form-category']//table//tr[.//td[contains(text(), 'Devices')]]/td[2]"
    DEVICES_DROPDOWN_MENU = By.XPATH, "//*[@id='autocomplete-category']/li/a"
    SEARCH_FIELD = By.XPATH, "//input[@name='search']"
    SEARCH_ICON = By.XPATH, "//i[@class='fa-solid fa-magnifying-glass']"
    ALERT = By.XPATH, "//*[@id='alert']/div"
    SEARCH_HEADER = By.XPATH, "//*[@id='content']/h1"
    SAVE_BUTTON = By.XPATH, "//*[@id='content']//button[contains(@class, 'btn btn-primary') and @data-bs-original-title='Save']"
    DELETE_CHECKBOX = By.XPATH, ".//input[@type='checkbox' and @name='selected[]']"
    DELETE_PRODUCT_BUTTON = By.XPATH, "//*[@id='content']//button[contains(@class, 'btn btn-danger') and @data-bs-original-title='Delete']"
    TABLE_PRODUCT_ROW = By.XPATH, "//table//tbody/tr"
    TABLE_PRODUCT_NAME = By.XPATH, ".//td[3]"

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def open_admin_page(self):
        self.driver.get(self.BASE_URL + "/administration")

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

    def click_catalog(self, locator: tuple[str, str], menu_locator: tuple[str, str],
                      frame_locator: tuple[str, str] = None, max_attempts=3):
        for attempt in range(max_attempts):
            try:
                if frame_locator:
                    try:
                        frame = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located(frame_locator))
                        self.driver.switch_to.frame(frame)
                    except (TimeoutException, NoSuchFrameException) as e:
                        print(f"Ошибка при переключении на фрейм {frame_locator}: {e}")
                        pass
                element: WebElement = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located(locator))
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable(element))
                try:
                    self.driver.execute_script("arguments[0].click();", element)
                    return
                except StaleElementReferenceException as e:
                    print(f"StaleElementReferenceException при клике (попытка {attempt + 1}): {e}")
                    self._reopen_catalog(menu_locator)
                    continue
            except (TimeoutException, StaleElementReferenceException) as e:
                print(f"Ошибка (попытка {attempt + 1}): {e}")
                self._reopen_catalog(menu_locator)
                continue
            finally:
                try:
                    if frame_locator:
                        self.driver.switch_to.default_content()
                except Exception as e:
                    print(f"Не удалось вернуться к основному контенту: {e}")
        print(f"Не удалось кликнуть на элемент после {max_attempts} попыток с локатором {locator}")

    def _reopen_catalog(self, catalog_menu_locator: tuple[str, str]):
        try:
            catalog_menu: WebElement = WebDriverWait(self.driver, 1).until(
                EC.element_to_be_clickable(catalog_menu_locator))
            self.driver.execute_script("arguments[0].click();", catalog_menu)
        except TimeoutException:
            pass
        except StaleElementReferenceException:
            pass

    # Гигафункция
    def delete_products_by_name(self, product_names: list[str], product_row_locator: tuple[str, str],
                                checkbox_locator: tuple[str, str], delete_button_locator: tuple[str, str],
                                product_name_locator: tuple[str, str], frame_locator: tuple[str, str] = None):
        if frame_locator:
            try:
                frame = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(frame_locator))
                self.driver.switch_to.frame(frame)
            except TimeoutException as e:
                print(f"Ошибка при переключении на фрейм {frame_locator}: {e}")
                return
        try:
            for product_name in product_names:
                try:
                    product_rows = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_all_elements_located(product_row_locator))
                    print(f"Найдено {len(product_rows)} строк товаров.")
                    for row in product_rows:
                        try:
                            name_element = WebDriverWait(row, 1).until(
                                EC.presence_of_element_located(product_name_locator))
                            full_product_name = name_element.text.strip()
                            actual_product_name = full_product_name.splitlines()[0].strip()
                            if actual_product_name == product_name:
                                print(f"Товар '{product_name}' найден.")
                                try:
                                    checkbox = WebDriverWait(row, 1).until(EC.element_to_be_clickable(checkbox_locator))
                                    checkbox.click()
                                    print(f"Кликнут чекбокс для товара '{product_name}'.")
                                    break
                                except (NoSuchElementException, TimeoutException) as e:
                                    print(f"Не удалось найти или кликнуть чекбокс для товара '{product_name}': {e}")
                                    continue
                        except (NoSuchElementException, StaleElementReferenceException, TimeoutException) as e:
                            print(f"Ошибка при обработке строки товара '{product_name}': {e}")
                            continue
                except TimeoutException:
                    print("Не удалось найти строки товаров!")
                    continue
            try:
                delete_button = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(delete_button_locator))
                delete_button.click()
            except TimeoutException:
                print(f"Не удалось найти или нажать кнопку удаления: {delete_button_locator}")
                return
            try:
                alert = WebDriverWait(self.driver, 2).until(EC.alert_is_present())
                alert.accept()
            except TimeoutException:
                print("Alert не появился!")
            except Exception as e:
                print(f"Ошибка при обработке Alert: {e}")
        except TimeoutException:
            print("Не удалось найти строки товаров или кнопку удаления!")
        except UnexpectedAlertPresentException:
            try:
                alert = WebDriverWait(self.driver, 2).until(EC.alert_is_present())
                alert.accept()
            except TimeoutException:
                print("Alert не появился!")
            except Exception as e:
                print(f"Ошибка при обработке Alert: {e}")
        finally:
            if frame_locator:
                self.driver.switch_to.default_content()

    def login(self):
        self.driver.find_element(*self.USERNAME_FIELD).send_keys(self.USERNAME)
        self.driver.find_element(*self.PASSWORD_FIELD).send_keys(self.PASSWORD)
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def open_start_page(self):
        self.find_and_click_element(self.MAIN_PAGE_LINK)

    def open_main_page(self):
        self.driver.get(self.BASE_URL)

    def open_catalog(self, submenu_locator: tuple[str, str]):
        self.click_catalog(submenu_locator, self.CATALOG_MENU)

    def open_categories_page(self):
        self.open_catalog(self.CATEGORIES_SUBMENU)

    def open_products_page(self):
        self.open_catalog(self.PRODUCTS_SUBMENU)

    def click_save_button(self):
        self.find_and_click_element(self.SAVE_BUTTON)

    def click_add_button(self):
        self.find_and_click_element(self.ADD_BUTTON)

    def enter_name_and_meta_tag(self, name, meta_tag):
        self.driver.find_element(*self.PRODUCT_NAME_FIELD).send_keys(name)
        self.driver.find_element(*self.META_TAG_TITLE_FIELD).send_keys(meta_tag)

    def product_enter_seo_url(self, seo_url):
        self.find_and_click_element(self.PRODUCT_SEO_TAB)
        self.find_and_click_element(self.SEO_URL_FIELD)
        self.driver.find_element(*self.SEO_URL_FIELD).send_keys(seo_url)

    def category_enter_seo_url(self, seo_url):
        self.find_and_click_element(self.CATEGORY_SEO_TAB)
        self.find_and_click_element(self.SEO_URL_FIELD)
        self.driver.find_element(*self.SEO_URL_FIELD).send_keys(seo_url)

    def enter_model(self, model_name):
        self.find_and_click_element(self.PRODUCT_DATA_TAB)
        self.driver.find_element(*self.MODEL_FIELD).send_keys(model_name)

    def select_category(self, category_name):
        self.find_and_click_element(self.PRODUCT_LINKS_TAB)
        self.find_element(self.CATEGORIES_FIELD).send_keys(category_name)
        self.find_and_click_element(self.DEVICES_DROPDOWN_MENU)

    def add_new_category(self, category_name, seo_name):
        self.click_add_button()
        self.enter_name_and_meta_tag(category_name, category_name)
        self.category_enter_seo_url(seo_name)
        self.click_save_button()

    def add_new_product(self, product_name, category_name, seo_name):
        self.click_add_button()
        self.enter_name_and_meta_tag(product_name, product_name)
        self.enter_model(product_name)
        self.find_and_click_element(self.PRODUCT_LINKS_TAB)
        self.select_category(category_name)
        self.product_enter_seo_url(seo_name)
        self.click_save_button()

    def search(self, search_text):
        self.driver.find_element(*self.SEARCH_FIELD).send_keys(search_text)
        self.driver.find_element(*self.SEARCH_ICON).click()

    def devices_category_get_text(self):
        return self.find_element(self.DEVICES_CATEGORY).text

    def click_second_page_categories_table(self):
        self.find_and_click_element(self.CATEGORIES_TABLE_SECOND_PAGE)

    def click_second_page_products_table(self):
        self.find_and_click_element(self.PRODUCTS_TABLE_SECOND_PAGE)

    def get_alert_text(self):
        return self.driver.find_element(*self.ALERT).text

    def get_search_result_header_text(self):
        return self.driver.find_element(*self.SEARCH_HEADER).text


class TestAdminPage:
    @pytest.fixture(scope="session")
    def admin_page(self, driver):
        return AdminPage(driver)

    @pytest.mark.parametrize("category_name", ["Devices"])
    @pytest.mark.parametrize("seo_name", ["devices"])
    def test_add_devices_category(self, admin_page, category_name, seo_name):
        admin_page.open_admin_page()
        admin_page.login()
        admin_page.open_categories_page()
        admin_page.add_new_category(category_name, seo_name)
        admin_page.open_start_page()
        sleep(1)
        admin_page.open_categories_page()
        admin_page.click_second_page_categories_table()
        sleep(1)
        devices_category = admin_page.devices_category_get_text()
        assert devices_category == "Devices\nEnabled"

    @pytest.mark.parametrize("name, meta_tag, model, seo_url", [("Keyboard 1", "Keyboard 1", "Keyboard 1", "keyboard-1"),
                                                                ("Keyboard 2", "Keyboard 2", "Keyboard 2", "keyboard-2"),
                                                                ("Mouse 1", "Mouse 1", "Mouse 1", "mouse-1"),
                                                                ("Mouse 2", "Mouse 2", "Mouse 2", "mouse-2")])
    def test_add_product(self, admin_page, name, meta_tag, model, seo_url):
        admin_page.open_start_page()
        sleep(1)
        admin_page.open_products_page()
        admin_page.click_add_button()
        admin_page.enter_name_and_meta_tag(name, meta_tag)
        admin_page.enter_model(model)
        admin_page.select_category("Devices")
        admin_page.product_enter_seo_url(seo_url)
        admin_page.click_save_button()
        actual = admin_page.get_alert_text()
        assert actual == "Success: You have modified products!" or actual == "Warning: Please check the form carefully for errors!"

    @pytest.mark.parametrize("search_text", ["Keyboard 1", "Keyboard 2"])
    def test_search_added_products(self, admin_page, search_text):
        admin_page.open_main_page()
        admin_page.search(search_text)
        assert admin_page.get_search_result_header_text() == f"Search - {search_text}"

    @pytest.mark.parametrize("product_names", [["Product 8", "Keyboard 1", "Mouse 1"]])
    def test_delete_products(self, admin_page, product_names):
        admin_page.open_admin_page()
        admin_page.login()
        admin_page.open_products_page()
        admin_page.click_second_page_products_table()
        admin_page.delete_products_by_name(product_names, admin_page.TABLE_PRODUCT_ROW, admin_page.DELETE_CHECKBOX,
                                           admin_page.DELETE_PRODUCT_BUTTON, admin_page.TABLE_PRODUCT_NAME)
        actual = admin_page.get_alert_text()
        assert actual == "Success: You have modified products!"

    @pytest.mark.parametrize("search_text", ["Keyboard 2", "Mouse 2"])
    def search_deleted_products(self, admin_page, search_text):
        admin_page.open_main_page()
        admin_page.search(search_text)
        assert admin_page.get_search_result_header_text() == f"Search - {search_text}"


@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Firefox()
    driver.maximize_window()
    yield driver
    driver.quit()
