import logging
import time
import re
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from setuptools.errors import LinkError
from webdriver_manager.chrome import ChromeDriverManager
from wonderwords import RandomWord

class WebController:
    def __init__(self):
        """Initialize the WebController class."""

        self.db_path_directory = "C:\\Temp\\ContextoSolver"
        os.makedirs(self.db_path_directory, exist_ok=True)

        self.info_path_file = "C:\\Temp\\ContextoSolver\\logs.txt"
        with open(self.info_path_file, 'a') as f:
            f.write("\n" + "=" * 50 + " New Session " + "=" * 50 + "\n")

        file_handler = logging.FileHandler(self.info_path_file, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        logger = logging.getLogger()
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

    ########################################################################################################################

    def start_the_browser(self):
        try:
            browser_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
            options = Options()
            options.binary_location = browser_path
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.maximize_window()
        except FileNotFoundError:
            logging.warning("Brave browser not found at the default location. Google Chrome browser will be executed")
            try:
                self.driver = webdriver.Chrome()
            except Exception as e:
                logging.error("Chrome browser could not be found - start_the_browser(self) - failed: %s", e)
            else:
                self.driver.maximize_window()
                logging.info("Chrome browser is active")
        except Exception as e:
            logging.error("An unexpected error occurred: %s", e)



    def initiate_contexto(self):
        try:
            self.driver.get("https://contexto.me/")
            time.sleep(3)
        except Exception as e:
            logging.error("Failed to open the website: %s", e)
        else:
            try:
                self.driver.find_element(By.CLASS_NAME, 'fc-primary-button').click()
            except Exception:
                logging.error("Consent cookie button could not be pressed or found.")
                logging.error("Please press it manually if needed.")
            else:
                logging.info("Contexto is fully initiated and ready to use")
            finally:
                return "este asta un string?"


    def __click_yes_for_give_up(self):
        elements = self.driver.find_elements(By.CLASS_NAME, 'share-btn')
        for element in elements:
            if element.text == 'Yes':
                element.send_keys(Keys.RETURN)
                break

    def __insert_random_word(self):
        random_word = RandomWord().random_words(1, include_parts_of_speech=["nouns"])[0]
        logging.info("Random word: %s", random_word)
        elements = self.driver.find_elements(By.CLASS_NAME, 'word')
        for element in elements:
            element.send_keys(random_word, Keys.ENTER)
            break
        logging.info("Inserted random word: %s", random_word)

    def __load_data(self):
        try:
            with open(self.db_path_file, "r") as infile:
                return infile.read()
        except FileNotFoundError:
            logging.warning("File/directory not found. Creating new one.")
            os.makedirs(self.db_path_directory, exist_ok=True)
            with open(self.db_path_file, "w") as starting_file:
                pass
            return ""

    def __save_data(self, data):
        with open(self.db_path_file, "w") as outfile:
            outfile.write(data)

    def __add_data(self, new_data):
        data = self.__load_data()
        if isinstance(new_data, list):
            new_data = "\n".join(map(str, new_data))
        elif not isinstance(new_data, str):
            new_data = str(new_data)
        if new_data in data:
            logging.info("Data is already in the file. No changes made.")
        else:
            data += "\n" + new_data
            self.__save_data(data)
            logging.info("Data added successfully.")

    def add_data(self, new_data):
        data = self.__load_data()
        data += "\n" + new_data
        self.__save_data(data)

    def extract_test(self):
        self.click_3dots()
        self.click_give_up()
        time.sleep(3)
        self.click_closest_word()
        time.sleep(3)
        data = []
        elements = self.driver.find_elements(By.CLASS_NAME, 'row-wrapper')
        for element in elements:
            data.append(element.text.split('\n'))
        return list(dict.fromkeys(data))

    def click_3dots(self):
        elements = self.driver.find_elements(By.CLASS_NAME, 'btn')
        for element in elements:
            element.click()
            break

    def click_give_up(self):
        elements = self.driver.find_elements(By.CLASS_NAME, 'menu-item')
        for element in elements:
            if element.text == 'Give up':
                element.click()
                self.__click_yes_for_give_up()
                break

    def click_closest_word(self):
        elements = self.driver.find_elements(By.CLASS_NAME, 'button')
        for element in elements:
            if element.text == 'Closest words':
                element.send_keys(Keys.RETURN)
                break

    def click_previous_games(self):
        elements = self.driver.find_elements(By.CLASS_NAME, 'menu-item')
        for element in elements:
            if element.text == 'Previous games':
                element.click()
                break

    def click_desired_previous_games(self, game_number):
        elements = self.driver.find_elements(By.CLASS_NAME, 'game-selection-button')
        for element in elements:
            if re.search('#' + str(game_number) + '\n', element.text):
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                element.click()
                break

    def click_on_random_from_previous_games(self):
        elements = self.driver.find_elements(By.CLASS_NAME, 'button')
        for element in elements:
            if element.text == "Random":
                element.click()
                break

    def get_game_number(self):
        element = self.driver.find_element(By.XPATH, "//span[contains(text(), '#')]")
        return element.text.split('#')[1].strip()

    def click_on_x_to_close_previous_games(self):
        elements = self.driver.find_elements(By.CLASS_NAME, "modal-close-button")
        for element in elements:
            element.click()
            break

    def extract_data_from_game(self):
        self.click_3dots()
        self.click_give_up()
        time.sleep(3)
        self.click_closest_word()
        time.sleep(3)
        data = []
        elements = self.driver.find_elements(By.CLASS_NAME, 'row-wrapper')
        for element in elements:
            data.append(element.text.split('\n'))
        return list(dict.fromkeys(data))

    def extract_all_history_games(self):
        for _ in range(int(self.get_game_number())):
            time.sleep(1)
            try:
                data = self.extract_data_from_game()
                logging.info(data)
                self.__add_data(data)
            except Exception as e:
                logging.error("An unexpected error occurred: %s", e)
            else:
                self.click_on_x_to_close_previous_games()
                self.click_3dots()
                self.click_previous_games()
                time.sleep(1)
                self.click_desired_previous_games(int(self.get_game_number()) - 1)
                time.sleep(1)


#DE REPARAT SA SE OPREASCA CAND GASESTE UN CUVANT CA SA NU MEARGA LA INFINIT SI SA FIE UN UPDATE LOGIC + TO BE TESTED LEL

#