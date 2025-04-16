from time import sleep
from selenium.webdriver.remote.webelement import WebElement
from selenium.common import TimeoutException, NoSuchFrameException, StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
import pytest
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from Base_Page import BasePage
from selenium.webdriver.support import expected_conditions as EC


class YouTube(BasePage):
    SHORTS_TAB = By.XPATH, "//ytm-pivot-bar-item-renderer[.//c3-icon][2]"
    SHORTS_LIKE_BUTTON = By.XPATH, "//div[contains(@class, \"reel-player-overlay-actions\")]//button[contains(@aria-label, 'Видео')]"
    VIDEO_PREVIEW = By.XPATH, "//*[contains(@class, \"video-thumbnail-container-large\")]//img[contains(@class, \"yt-core-image\")]"
    VIDEO_PLAY_BUTTON = By.XPATH, "//button[@aria-label='Воспроизвести видео']"
    WATCH_BUTTON = By.XPATH, "//button[@aria-label='Смотреть']"
    NAVIGATOR_BUTTON = By.XPATH, "//div[contains(@class, \"chip-container\")]//c3-icon"
    TRENDING_TAB = By.XPATH, "//a[contains(@class, \"yt-spec-navigation-item-shape__navigation-item-endpoint\")]"
    SEARCH_ICON = By.XPATH, "//button[contains(@aria-label, 'Поиск на YouTube')]"
    SEARCH_FIELD = By.XPATH, "//form[contains(@class, \"ytSearchboxComponentSearchForm\")]//input"

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def open_youtube(self):
        self.driver.get(self.BASE_URL)

    def open_shorts_tab(self):
        self.driver.find_element(*self.SHORTS_TAB).click()

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


class TestYouTubeWeb:
    @pytest.fixture(scope="session")
    def youtube(self, driver):
        return YouTube(driver)

    def test_youtube_mobile(self, youtube, driver):
        youtube.open_youtube()
        assert "YouTube" in driver.title

    def test_open_shorts_tab(self, youtube, driver):
        youtube.open_youtube()
        youtube.open_shorts_tab()
        assert driver.find_element(*YouTube.SHORTS_LIKE_BUTTON).is_displayed()
        sleep(3)

    def test_open_navigator(self, youtube, driver):
        youtube.open_youtube()
        youtube.find_and_click_element(YouTube.NAVIGATOR_BUTTON)
        assert youtube.find_element(YouTube.TRENDING_TAB).is_displayed()

    def test_search(self, youtube, driver):
        youtube.open_youtube()
        sleep(2)
        youtube.find_and_click_element(YouTube.SEARCH_ICON)
        youtube.find_element(YouTube.SEARCH_FIELD).send_keys("4k video")
        youtube.find_element(YouTube.SEARCH_FIELD).send_keys(Keys.RETURN)
        sleep(2)
        assert "4k video - YouTube" in driver.title

    def test_video_play(self, youtube, driver):
        youtube.open_youtube()
        youtube.find_and_click_element(YouTube.VIDEO_PREVIEW)
        assert youtube.find_element(YouTube.WATCH_BUTTON).is_displayed() or youtube.find_element(YouTube.VIDEO_PLAY_BUTTON).is_displayed()


@pytest.fixture(scope="session")
def driver():
    firefox_options = FirefoxOptions()
    firefox_options.set_preference("general.useragent.override", "Mozilla/5.0 (Android 13; Mobile; rv:125.0) Gecko/125.0 Firefox/125.0")
    driver = webdriver.Firefox(options=firefox_options)
    driver.implicitly_wait(10)
    driver.set_window_size(375, 667)
    yield driver
    driver.quit()
