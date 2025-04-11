from selenium.webdriver.support.wait import WebDriverWait
import pytest
import json
from appium.webdriver.common.appiumby import AppiumBy
from appium import webdriver
from appium.webdriver.webdriver import AppiumOptions
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.extensions.action_helpers import *

APPIUM_SERVER_URL = "http://localhost:4723"
PARAMS_FILE = "params.json"

SHORTS_PLAYER = AppiumBy.XPATH, "//android.view.ViewGroup[@resource-id=\"com.google.android.youtube:id/reel_watch_player\"]/android.widget.FrameLayout"
APP_BACKGROUND = AppiumBy.XPATH, "//android.widget.FrameLayout[@resource-id=\"android:id/content\"]"
SEARCH_ICON = AppiumBy.ACCESSIBILITY_ID, "Search"
SEARCH_TEXT = AppiumBy.ID, "com.google.android.youtube:id/search_edit_text"
VIDEO_PLAYER = AppiumBy.ID, "com.google.android.youtube:id/player_view"
FIRST_VIDEO_IN_SEARCH = AppiumBy.XPATH, "//android.support.v7.widget.RecyclerView[@resource-id=\"com.google.android.youtube:id/results\"]/android.view.ViewGroup[1]"
CHANNEL_NAME = AppiumBy.XPATH, "//android.support.v7.widget.RecyclerView[@resource-id=\"com.google.android.youtube:id/watch_list\"]/android.view.ViewGroup[2]/android.view.ViewGroup"
CHANNEL_INFO = AppiumBy.ID, "com.google.android.youtube:id/collapsing_header_container"

@pytest.fixture(scope="session")
def driver():
    with open(PARAMS_FILE, 'r') as f:
        params = json.load(f)

    appium_options = AppiumOptions()
    appium_options.load_capabilities(params)

    driver = webdriver.Remote(APPIUM_SERVER_URL, options=appium_options)
    yield driver
    driver.quit()


class TestYouTubeGestures:
    def test_scroll_down(self, driver):
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(APP_BACKGROUND))

        screen_size = driver.get_window_size()
        start_x = screen_size["width"] // 2
        start_y = screen_size["height"] // 2
        end_x = screen_size["width"] // 2
        end_y = int(screen_size["height"] * 0.2)

        for _ in range(1):
            finger = PointerInput(interaction.POINTER_TOUCH, "finger")
            actions = ActionChains(driver)
            actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        assert True

    def test_scroll_up(self, driver):
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(APP_BACKGROUND))

        screen_size = driver.get_window_size()
        start_x = screen_size["width"] // 2
        start_y = int(screen_size["height"] * 0.2)
        end_x = screen_size["width"] // 2
        end_y = int(screen_size["height"] * 0.8)

        for _ in range(1):
            finger = PointerInput(interaction.POINTER_TOUCH, "finger")
            actions = ActionChains(driver)
            actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        assert True

    def test_search_open_video(self, driver):
        search_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(SEARCH_ICON))
        search_button.click()

        search_field = WebDriverWait(driver, 5).until(EC.presence_of_element_located(SEARCH_TEXT))
        search_field.send_keys("4k video")

        driver.press_keycode(66)

        first_result = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(FIRST_VIDEO_IN_SEARCH))
        first_result.click()

        WebDriverWait(driver, 5).until(EC.presence_of_element_located(VIDEO_PLAYER))
        assert True

    def test_tap_channel(self, driver):
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(VIDEO_PLAYER))
        try:
            channel_name = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(CHANNEL_NAME))
            channel_name.click()

            WebDriverWait(driver, 5).until(EC.presence_of_element_located(CHANNEL_INFO))
            assert True
        except:
            assert False

    def test_swipe_shorts(self, driver):
        shorts_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Shorts")))
        shorts_button.click()

        WebDriverWait(driver, 3).until(EC.presence_of_element_located(SHORTS_PLAYER))

        screen_size = driver.get_window_size()
        start_x = screen_size["width"] // 2
        start_y = screen_size["height"] // 2
        end_x = screen_size["width"] // 2
        end_y = screen_size["height"] + 100

        finger = PointerInput(interaction.POINTER_TOUCH, "finger")
        actions = ActionChains(driver)
        actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

        try:
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Shorts")))
            assert True
        except:
            assert False
