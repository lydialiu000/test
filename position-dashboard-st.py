import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class TestPositionDashboardFunctions(unittest.TestCase):

    def setUp(self):
        self.service = webdriver.chrome.service.Service(executable_path=r'C:\Projects\gso-eui-testing\chromedriver.exe')
        self.service.start()
        chrome_options = Options()
        chrome_options.debugger_address = 'localhost:9222'
        chrome_options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        # chrome_options.add_argument("--disable-infobars")
        capabilities = chrome_options.to_capabilities()
        # ## remote for embedded testing
        self.driver = webdriver.Remote(command_executor=self.service.service_url, desired_capabilities=capabilities)
       
        # #for web page testing
        # self.driver = webdriver.Chrome()
        # self.driver.get('http://vmsfgenuidev2/loanAdministration/positions')
        # self.driver.maximize_window()
        # time.sleep(3)
    def test_basic_workflow(self):
        driver = self.driver
        driver.find_element_by_xpath("//button[text()='Apply']").click()
        ele = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[text()='Amazon.com Inc Revolver 2025']"))
        )

        # time.sleep(8)
        # ele = driver.find_element_by_xpath("//div[text()='Amazon.com Inc Revolver 2025']")
        ele.click()

        action = ActionChains(driver)
        # time.sleep(8)
        contract = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[text()='AMZN_Rev_01032017']"))
        )
        # contract = driver.find_element_by_xpath("//div[text()='AMZN_Rev_01032017']")
        
        action.context_click(contract).perform()
        initDrawdown = driver.find_element_by_xpath("//li[text()='Process Additional Drawdown']")
        action.move_to_element(initDrawdown).click().perform()

        driver.find_element_by_xpath("//button[text()='Zoom to Credit Contract']").click()


    # def tearDown(self):
        # self.driver.close()
        # self.service.stop()


if __name__=='__main__':
    unittest.main()