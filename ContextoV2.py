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
print(WebControllerObject.extract_data_from_the_game())