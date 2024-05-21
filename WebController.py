from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import re
import os


class WebController:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def initiate_contexto(self):
        self.driver.get("https://contexto.me/")
        self.driver.maximize_window()
        time.sleep(3)
        try:
            self.driver.find_element(By.CLASS_NAME, 'fc-primary-button').click()
        except:
            print("Consent cookie button could not be pressed. initiate_contexto() failed")
        else:
            print("Contexto is fully initiated and ready to use")

    def click_3dots(self):
        elements = self.driver.find_elements(By.CLASS_NAME, 'btn')
        for e in elements:
            e.click()
            break

    def click_previous_games(self):
        self.__click_3dots()
        elements = self._driver.find_elements(By.CLASS_NAME, 'menu-item')
        for e in elements:
            if e.text == 'Previous games':
                e.click()
                break

    def __click_yes_for_give_up(self):
        elements = self.driver.find_elements(By.CLASS_NAME, 'share-btn')
        for e in elements:
            if e.text == 'Yes':
                e.click()









