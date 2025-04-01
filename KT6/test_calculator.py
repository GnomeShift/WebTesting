import pytest
import json
from appium.webdriver.common.appiumby import AppiumBy
from appium import webdriver
from appium.webdriver.webdriver import AppiumOptions

APPIUM_SERVER_URL = "http://localhost:4723"
PARAMS_FILE = "params.json"

DIGIT_1 = "com.google.android.calculator:id/digit_1"
DIGIT_2 = "com.google.android.calculator:id/digit_2"
DIGIT_3 = "com.google.android.calculator:id/digit_3"
DIGIT_4 = "com.google.android.calculator:id/digit_4"
DIGIT_5 = "com.google.android.calculator:id/digit_5"
DIGIT_6 = "com.google.android.calculator:id/digit_6"
DIGIT_7 = "com.google.android.calculator:id/digit_7"
DIGIT_8 = "com.google.android.calculator:id/digit_8"
DIGIT_9 = "com.google.android.calculator:id/digit_9"
DIGIT_0 = "com.google.android.calculator:id/digit_0"
PLUS_BUTTON = "plus"
MINUS_BUTTON = "minus"
MULTIPLY_BUTTON = "multiply"
DIVIDE_BUTTON = "divide"
CLEAR_BUTTON = "com.google.android.calculator:id/del"
EQUALS_BUTTON = "equals"
RESULT_FIELD = "com.google.android.calculator:id/result_final"
FORMULA_FIELD = "com.google.android.calculator:id/formula"


@pytest.fixture(scope="session")
def driver():
    with open(PARAMS_FILE, 'r') as f:
        params = json.load(f)

    appium_options = AppiumOptions()
    appium_options.load_capabilities(params)

    driver = webdriver.Remote(APPIUM_SERVER_URL, options=appium_options)
    yield driver
    driver.quit()


class TestCalculator:
    @pytest.mark.parametrize("digit_1, digit_2, operation, expected", [(DIGIT_2, DIGIT_2, PLUS_BUTTON, "4"),
                                                                       (DIGIT_5, DIGIT_3, MINUS_BUTTON, "2"),
                                                                       (DIGIT_4, DIGIT_8, MULTIPLY_BUTTON, "32"),
                                                                       (DIGIT_7, DIGIT_1, DIVIDE_BUTTON, "7")])
    def test_calculator(self, driver, digit_1, digit_2, operation, expected):
        driver.find_element(by=AppiumBy.ID, value=digit_1).click()
        driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=operation).click()
        driver.find_element(by=AppiumBy.ID, value=digit_2).click()
        driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=EQUALS_BUTTON).click()
        result = driver.find_element(by=AppiumBy.ID, value=RESULT_FIELD).text
        assert result == expected

    def test_clear(self, driver):
        driver.find_element(by=AppiumBy.ID, value=DIGIT_6).click()
        driver.find_element(by=AppiumBy.ID, value=CLEAR_BUTTON).click()
        result = driver.find_element(by=AppiumBy.ID, value=FORMULA_FIELD).text
        assert result == ""
