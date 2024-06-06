from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from random_word import RandomWords
import time
import re
import os
import random


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
        finally:
            return "string?"

##########################################################################
#
#   Privat funtions for different actions
#

    def __click_yes_for_give_up(self):
        elements = self.driver.find_elements(By.CLASS_NAME, 'share-btn')
        for e in elements:
            if e.text == 'Yes':
                e.send_keys(Keys.RETURN)
                #e.click()
                break

    def __insert_a_random_word(self):
        r = RandomWords()
        random_word = r.get_random_word()
        print("In random_word avem : " + random_word)
        elements = self.driver.find_elements(By.CLASS_NAME, 'word')
        for e in elements:
            e.send_keys(random_word, Keys.ENTER)
            break
        print("Cuvantul random introdus a fost " + random_word)

#
#   End of privat functions
#
##########################################################################
#
# Start of basic functions like click on diffrent buttons or simple actions like go to x game
#
    def click_3dots(self):
        elements = self.driver.find_elements(By.CLASS_NAME, 'btn')
        for e in elements:
            e.click()
            break

    def click_give_up(self):
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
        elements = self.driver.find_elements(By.CLASS_NAME, 'menu-item')
        for e in elements:
            if e.text == 'Previous games':
                e.click()
                break
    def click_desired_previous_games(self, game_number):
        elements = self.driver.find_elements(By.CLASS_NAME, 'game-selection-button')
        for e in elements:
            if re.search('#' + str(game_number) + '\n', e.text) is not None:
                self.driver.execute_script("arguments[0].scrollIntoView();", e)
                e.click()
                break
    def click_on_random_from_previous_games(self):
        elements = self.driver.find_elements(By.CLASS_NAME, 'button')
        for e in elements:
            if e.text == "Random":
                e.click()
                break

    def get_game_number(self):
        elements = self.driver.find_element(By.XPATH, "//span[contains(text(), '#')]")
        gamenumber = elements.text.split('#')[1].strip()
        print(gamenumber)
        return gamenumber

#
#   End of basic functions
#
##########################################################################
#
# Start of complex functions such as extracting data
#

    def extract_data_from_the_game(self):
        self.click_3dots()
        self.click_give_up()
        time.sleep(3)
        self.click_closest_word()
        time.sleep(3)
        #
        data = []
        elements = self.driver.find_elements(By.CLASS_NAME, 'row-wrapper')
        for e in elements:
            data.append(e.text.split('\n'))
        res = []
        [res.append(x) for x in data if x not in res]
        return res