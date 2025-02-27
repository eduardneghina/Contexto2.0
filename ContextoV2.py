import time

from GameController import *


if __name__ == "__main__":

    GameControllerObject = GameController()
    GameControllerObject.start_the_game()
    GameControllerObject.first_word_insert_to_start()
    time.sleep(20)
