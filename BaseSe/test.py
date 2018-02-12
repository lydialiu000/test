from BaseSe.Selenium3 import SeleniumBase
from selenium.webdriver.common.by import By

def testse(self):
    search_ele = (By.XPATH, "//button[text()='Apply']")
    self.find_element(*self,search_ele)


# testse()