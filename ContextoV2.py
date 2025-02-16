import time
from WebController import *


WebControllerObject = WebController()
WebControllerObject.start_the_browser()
WebControllerObject.initiate_contexto()
#print(WebControllerObject.extract_the_word_list_from_the_game_number())
print(WebControllerObject.extract_all_history_games())

time.sleep(10)