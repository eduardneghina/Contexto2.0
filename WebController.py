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

        self.path_directory = "C:\\Temp\\ContextoSolver"
        os.makedirs(self.path_directory, exist_ok=True)

        self.database_path_file = "C:\\Temp\\ContextoSolver\\database.txt"
        with open(self.database_path_file, 'a') as f:
            pass

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



    def extract_all_history_games(self):
        current_game_number = int(self.__get_game_number())
        existing_data = self.__load_data()
        all_games_exist = True

        for game_number in range(current_game_number, -1, -1):
            if re.search(rf"^#{game_number}\b", existing_data, re.MULTILINE):
                logging.info(f"Game number {game_number} already exists in the database.")
                continue
            else:
                all_games_exist = False

            self.__click_3dots()
            time.sleep(1)
            self.__click_previous_games()
            time.sleep(1)
            self.__click_desired_previous_games(game_number)
            time.sleep(1)
            self.__click_3dots()
            time.sleep(1)
            self.__click_give_up()
            time.sleep(1)
            self.__click_closest_words()
            time.sleep(1)
            word_list = self.__extract_the_word_list_from_the_game_number()
            time.sleep(1)
            data_line = f"#{game_number} {word_list}\n"
            print(f"Data added: {data_line}")
            time.sleep(1)
            self.__add_data(data_line)
            time.sleep(1)
            self.__click_close_closest_words()
            time.sleep(1)

        if all_games_exist:
            logging.info("All games are already in the database. Exiting method.")



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

    def insert_a_word(self, word):
        elements = self.driver.find_elements(By.CLASS_NAME, 'word')
        for element in elements:
            element.send_keys(str(word))
            element.send_keys(Keys.ENTER)
            time.sleep(1)

    def __load_data(self):
        """Load data from the database file."""
        if not os.path.exists(self.database_path_file):
            logging.warning("File/directory not found. Creating new one.")
            os.makedirs(self.path_directory, exist_ok=True)
            with open(self.database_path_file, "w") as starting_file:
                pass
            return ""

        try:
            with open(self.database_path_file, "r") as infile:
                return infile.read()
        except Exception as e:
            logging.error("An error occurred while reading the file: %s", e)
            return ""

    def __save_data(self, data):
        with open(self.database_path_file, "w") as outfile:
            outfile.write(data)

    def __add_data(self, new_data):
        existing_data = self.__load_data()
        new_data = "\n" + new_data if existing_data else new_data
        updated_data = new_data + existing_data
        sorted_data = sorted(
            updated_data.splitlines(),
            key=lambda x: int(re.search(r'#(\d+)', x).group(1)) if re.search(r'#(\d+)', x) else -1,
            reverse=True
        )
        self.__save_data("\n".join(sorted_data))

    def __extract_the_word_list_from_the_game_number(self):
        data = []
        elements = self.driver.find_elements(By.CLASS_NAME, 'row-wrapper')
        for element in elements:
            data.append(tuple(element.text.split('\n')))
        return list(dict.fromkeys(data))

    def __click_3dots(self):
        elements = self.driver.find_elements(By.CLASS_NAME, 'btn')
        for element in elements:
            element.click()
            break

    def __click_give_up(self):
        elements = self.driver.find_elements(By.CLASS_NAME, 'menu-item')
        for element in elements:
            if element.text == 'Give up':
                element.click()
                self.__click_yes_for_give_up()
                break

    def __click_closest_words(self):
        elements = self.driver.find_elements(By.CLASS_NAME, 'button')
        for element in elements:
            if element.text == 'Closest words':
                element.send_keys(Keys.RETURN)
                break

    def __click_close_closest_words(self):
        elements = self.driver.find_elements(By.CLASS_NAME, 'modal-close-button')
        for element in elements:
            element.click()
            break

    def __click_previous_games(self):
        elements = self.driver.find_elements(By.CLASS_NAME, 'menu-item')
        for element in elements:
            if element.text == 'Previous games':
                element.click()
                break

    def __click_desired_previous_games(self, game_number):
        elements = self.driver.find_elements(By.CLASS_NAME, 'game-selection-button')
        for element in elements:
            if re.search('#' + str(game_number) + '\n', element.text):
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                element.click()
                break

    def __click_on_random_from_previous_games(self):
        elements = self.driver.find_elements(By.CLASS_NAME, 'button')
        for element in elements:
            if element.text == "Random":
                element.click()
                break

    def __get_game_number(self):
        element = self.driver.find_element(By.XPATH, "//span[contains(text(), '#')]")
        return element.text.split('#')[1].strip()

    def __click_on_x_to_close_previous_games(self):
        elements = self.driver.find_elements(By.CLASS_NAME, "modal-close-button")
        for element in elements:
            element.click()
            break

    def clear_text_area(self):
        elements = self.driver.find_elements(By.CLASS_NAME, 'word')
        for e in elements:
            e.clear()

    def read_returned_text_for_first_try(self):
        elements = self.driver.find_elements(By.CLASS_NAME, 'message-text')
        for element in elements:
            return element.text

    def get_word_and_id(self):
        elements = self.driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[4]/div/div/div[2]')
        for e in elements:
            if e is not None:
                a = e.text.split()
                return a
