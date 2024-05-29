import time

from WebController import *


# driver = initiate_contexto()

driver = WebController()
driver.initiate_contexto()
time.sleep(3)
driver.click_3dots()
time.sleep(1)
driver.click_previous_games()
time.sleep(1)
driver.click_desired_previous_games(9)
time.sleep(2)
driver.get_game_number()
time.sleep(4)


