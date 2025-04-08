import os

class BasePage:
    BASE_URL = "http://192.168.0.225:8081"
    SELENOID_URL = "http://192.168.0.225:4444/wd/hub"

    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(2)
        self.driver.get(BasePage.BASE_URL)

    def screenshot(self, filename, folder_name="screens"):
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)

        self.driver.save_screenshot(os.path.join(folder_name, filename))
