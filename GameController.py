from WebController import *
from AI import *
import random

class GameController:
    def __init__(self):
        self._web_controller = WebController()
        self._ai = AI()

    async def start_the_game(self):
        self._web_controller.start_the_browser()
        self._web_controller.initiate_contexto()

    async def first_word_insert_to_start(self):
        # class 'list'
        all_words_from_history = await self._ai.return_all_words_from_database_no_duplicates_alphabetically()
        # class 'str'
        random_word_to_be_inserted_for_the_game_start = random.choice(all_words_from_history)
        # insert the random word
        self._web_controller.insert_a_word(random_word_to_be_inserted_for_the_game_start)
        if self._web_controller.read_returned_text_for_first_try() == "I'm sorry, I don't know this word":
            print("The word was not accepted. Trying again.")
            self._web_controller.clear_text_area()
            await self.first_word_insert_to_start()
        else:
            print("The game has started successfully.")
            print("The first word inserted was: " + random_word_to_be_inserted_for_the_game_start)
            return True