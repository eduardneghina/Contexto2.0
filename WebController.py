from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import re
import os


def initiate_contexto():
    driver = webdriver.Chrome()
    driver.get('https://contexto.me/')
    driver.maximize_window()
    time.sleep(3)
    driver.find_element(By.CLASS_NAME, 'fc-primary-button').click()
    time.sleep(3)