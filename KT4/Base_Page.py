from selenium import webdriver


class BasePage:
    BASE_URL = "http://192.168.0.225:8081"

    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(3)
        self.driver.get(BasePage.BASE_URL)
