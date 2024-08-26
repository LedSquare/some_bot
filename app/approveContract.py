from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint
import os, time, asyncio, re


async def approveContract(driver: webdriver, contractId: str) -> bool: 
    
    if driver.current_url == 'https://1sed.infogeneral.ru/auth/login':
        await login(driver)
        
    search_input = driver.find_element(By.ID, 'quick-search')
    search_input.send_keys(contractId, Keys.ENTER)

    await asyncio.sleep(1.5)

    try:
        status = driver.find_element(By.XPATH, value="//blockquote[@class='this group']")
    except (NoSuchElementException):
        groups = driver.find_elements(By.XPATH, value="//blockquote[@class=' group']")
        status = groups[-1]
        if not groups:
            return False

    regex = r"ИО Завершено\s*(.*)"

    if re.search(regex, status.text):
        driver.find_element(By.ID, 'addRouteField').click()

        await asyncio.sleep(12)

        driver.find_element(By.ID, 'routeButtonGroup').click()
        driver.find_element(By.XPATH, value="//i[@class='icon-']").click()

        await asyncio.sleep(0.5)

        driver.find_element(By.ID, value="yt1").click()
        
        await asyncio.sleep(10)

        return True

    elif status.text == 'ИО На рассмотрении': 
        driver.find_element(By.ID, 'routeButtonGroup').click()
        driver.find_element(By.XPATH, value="//i[@class='icon-']").click()

        await asyncio.sleep(0.5)

        driver.find_element(By.ID, value="yt1").click()
        
        await asyncio.sleep(10)

        return True
    
    else: 
        return False

async def login(driver: webdriver):
    LOGIN = os.getenv('LOGIN')
    PASSWORD = os.getenv('PASSWORD')

    driver.find_element(By.ID, 'LoginForm_username').send_keys(LOGIN)
    driver.find_element(By.ID, 'LoginForm_password').send_keys(PASSWORD)
    driver.find_element(By.NAME, 'yt0').click()

    await asyncio.sleep(1)
