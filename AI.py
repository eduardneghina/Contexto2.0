"""
"""
class AI():
    def __init__(self):




        self.driver.get("https://contexto.me/")
        time.sleep(3)
        try:
            self.driver.find_element(By.CLASS_NAME, 'fc-primary-button').click()
        except Exception:
            logging.error("Consent cookie button could not be pressed. initiate_contexto() failed")
        else:
            logging.info("Contexto is fully initiated and ready to use")
        return "este asta un string?"







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