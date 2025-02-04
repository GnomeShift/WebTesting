
from selenium.common import NoSuchElementException
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import pytest

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Firefox()
    driver.implicitly_wait(3)
    driver.get("http://192.168.0.225:8081/")
    yield driver
    driver.close()

def test_switch_screens(driver):
    driver.get("http://192.168.0.225:8081/en-gb/product/macbook?search=MacBook")
    driver.find_element(By.XPATH, "//*[@id='content']/div[1]/div[1]/div/a/img").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div/button[2]").click()

    # Счетчик фото
    counter = driver.find_element(By.XPATH, "//div[text()='2 of 5']")
    expected = "2 of 5"
    assert counter.text == expected

def test_switch_screens_negative(driver):
    driver.get("http://192.168.0.225:8081/en-gb/product/macbook?search=MacBook")
    try:
        driver.find_element(By.XPATH, "//img[@title='MacBook Pro']").click()
    except NoSuchElementException:
        assert True

def test_switch_currency(driver):
    driver.find_element(By.CLASS_NAME, "dropdown-toggle").click()
    driver.find_element(By.XPATH, "//a[@href='EUR']").click()

    # Значок валюты
    expected = "€"
    actual = driver.find_element(By.XPATH, "//strong").text
    assert actual == expected

def test_switch_currency_negative(driver):
    driver.find_element(By.CLASS_NAME, "dropdown-toggle").click()
    driver.find_element(By.XPATH, "//a[@href='EUR']").click()

    # Значок валюты
    expected = "$"
    actual = driver.find_element(By.XPATH, "//strong").text
    assert actual != expected

def test_page_pc(driver):
    driver.find_element(By.XPATH, "//a[@href='http://192.168.0.225:8081/en-gb/catalog/desktops']").click()
    driver.find_element(By.XPATH, "//a[@href='http://192.168.0.225:8081/en-gb/catalog/desktops/pc']").click()

    # Текст на странице
    expected = ("Desktops\n"
                "Example of category description text\n"
                "There are no products to list in this category.\n"
                "Continue")
    actual = driver.find_element(By.ID, "content").text
    assert actual == expected

def test_page_pc_negative(driver):
    driver.find_element(By.XPATH, "//a[@href='http://192.168.0.225:8081/en-gb/catalog/desktops']").click()
    driver.find_element(By.XPATH, "//a[@href='http://192.168.0.225:8081/en-gb/catalog/desktops/pc']").click()

    # Текст на странице
    expected = "There are nothing."
    actual = driver.find_element(By.ID, "content").text
    assert actual != expected

def test_signup(driver):
    first_name = "Test"
    last_name = "Test"
    email = "123@example.com"
    password = "123123"

    driver.find_element(By.XPATH, "//span[text()='My Account']").click()
    driver.find_element(By.XPATH, "//a[text()='Register']").click()

    # Заполняем форму регистрации
    driver.find_element(By.XPATH, "//input[@name='firstname']").send_keys(first_name)
    driver.find_element(By.XPATH, "//input[@name='lastname']").send_keys(last_name)
    driver.find_element(By.XPATH, "//input[@name='email']").send_keys(email)
    driver.find_element(By.XPATH, "//input[@name='password']").send_keys(password)
    driver.find_element(By.XPATH, "//input[@name='agree']").send_keys(Keys.SPACE)
    driver.find_element(By.XPATH, "//button[text()='Continue']").submit()
    driver.implicitly_wait(3)

    actual = driver.find_element(By.XPATH, "//*[@id='content']/h1")
    assert actual.is_displayed() == True

def test_signup_negative(driver):
    first_name = "Test"
    last_name = "Test"
    email = "123@example.com"
    password = ""

    driver.find_element(By.XPATH, "//span[text()='My Account']").click()
    driver.find_element(By.XPATH, "//a[text()='Register']").click()

    # Заполняем форму регистрации
    driver.find_element(By.XPATH, "//input[@name='firstname']").send_keys(first_name)
    driver.find_element(By.XPATH, "//input[@name='lastname']").send_keys(last_name)
    driver.find_element(By.XPATH, "//input[@name='email']").send_keys(email)
    driver.find_element(By.XPATH, "//input[@name='password']").send_keys(password)
    driver.find_element(By.XPATH, "//input[@name='agree']").send_keys(Keys.SPACE)
    driver.find_element(By.XPATH, "//button[text()='Continue']").submit()

    expected = "Password must be between 4 and 20 characters!"
    actual = driver.find_element(By.XPATH, "//div[text()='Password must be between 4 and 20 characters!']").text
    assert actual == expected

def test_search(driver):
    text = "MacBook"
    driver.find_element(By.XPATH, "//input[@name='search']").send_keys(text)
    driver.find_element(By.XPATH, "//i[@class='fa-solid fa-magnifying-glass']").click()

    # Поисковая строка
    expected = "Search - MacBook"
    actual = driver.find_element(By.XPATH, "//*[@id='content']/h1").text
    assert actual == expected

def test_search_negative(driver):
    text = "iPhone"
    driver.find_element(By.XPATH, "//input[@name='search']").send_keys(text)
    driver.find_element(By.XPATH, "//i[@class='fa-solid fa-magnifying-glass']").click()

    # Поисковая строка
    expected = "Search - MacBook"
    actual = driver.find_element(By.XPATH, "//*[@id='content']/h1").text
    assert actual != expected
