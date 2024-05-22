from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import os


class WebController:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def initiate_contexto(self):
        self.driver.get("https://contexto.me/")
        self.driver.maximize_window()
        elements = self.driver.find_element(By.XPATH, "//span[contains(text(), '#')]")
        gamenumber = elements.text.split('#')[1].strip()
        time.sleep(3)
        try:
            self.driver.find_element(By.CLASS_NAME, 'fc-primary-button').click()
        except:
            print("Consent cookie button could not be pressed. initiate_contexto() failed")
        else:
            print("Contexto is fully initiated and ready to use")
            return gamenumber

    def click_3dots(self):
        elements = self.driver.find_elements(By.CLASS_NAME, 'btn')
        for e in elements:
            e.click()
            break


    def __click_yes_for_give_up(self):
        elements = self.driver.find_elements(By.CLASS_NAME, 'share-btn')
        for e in elements:
            if e.text == 'Yes':
                e.send_keys(Keys.RETURN)
                #e.click()
                break

    def click_give_up(self):
        #self.click_3dots()
        elements = self.driver.find_elements(By.CLASS_NAME, 'menu-item')
        for e in elements:
            if e.text == 'Give up':
                e.click()
                self.__click_yes_for_give_up()
                break

    def click_closest_word(self):
        elements = self.driver.find_elements(By.CLASS_NAME, 'button')
        for e in elements:
            if e.text == 'Closest words':
                e.send_keys(Keys.RETURN)
                #e.click() == The element must be visible on the page, ads or outscrolled elements can't be clicked. Use key return instead or Actions class
                break
    def click_previous_games(self):
        self.click_3dots()
        elements = self.driver.find_elements(By.CLASS_NAME, 'menu-item')
        for e in elements:
            if e.text == 'Previous games':
                e.click()
                break
    def click_desired_previous_games(self, game_number):
        #self.click_previous_games()
        elements = self.driver.find_elements(By.CLASS_NAME, 'game-selection-button')
        for e in elements:
            if re.search('#' + str(game_number) + '\n', e.text) is not None:
                self.driver.execute_script("arguments[0].scrollIntoView();", e)
                e.click()
                break

    def update_all_words(self):
        gamenumber_str = self.initiate_contexto()
        gamenumber = int(gamenumber_str)
        for e in range(gamenumber) :
            print("Suntem la game-ul cu nr", e)
            self.click_previous_games()
            time.sleep(1)
            self.click_desired_previous_games(e)
            time.sleep(1)
            self.click_3dots()
            time.sleep(1)
            self.click_give_up()
            time.sleep(1)
            self.click_closest_word()
            time.sleep(1)
            print("dada")
