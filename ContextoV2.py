import time
from WebController import *



#############################################################
########### reminder for future #########################################
#############################################################
# _driver = driver.initiate_contexto()
# print(_driver)
# output "string" - see initiate_contexto(self): finally
#
#
#
#
#####################################################

WebControllerObject = WebController()
WebControllerObject.initiate_contexto()



WebControllerObject.extract_all_history_games()
