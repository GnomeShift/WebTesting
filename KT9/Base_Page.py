class BasePage:
    BASE_URL = "https://youtube.com"

    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(2)
        self.driver.get(BasePage.BASE_URL)
