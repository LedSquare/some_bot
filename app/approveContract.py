from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, time

def approveContract(driver: webdriver, contractId: str) -> bool: 

    if driver.current_url == 'https://1sed.infogeneral.ru/auth/login':
        login(driver)

    search_input = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'quick-search'))
    )
    
    search_input.send_keys(contractId, Keys.ENTER)

    try:
        status = driver.find_element(By.XPATH, value="//blockquote[@class='this group']")

    except (NoSuchElementException) as e:
        return False

    if status.text != 'ИО На рассмотрении':
        return False

    return True

def login(driver: webdriver) -> None:
    LOGIN = os.getenv('LOGIN')
    PASSWORD = os.getenv('PASSWORD')

    driver.find_element(By.ID, 'LoginForm_username').send_keys(LOGIN)
    driver.find_element(By.ID, 'LoginForm_password').send_keys(PASSWORD)
    driver.find_element(By.NAME, 'yt0').click()

    time.sleep(1)