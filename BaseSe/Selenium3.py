#!/usr/bin/python3
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait

class SeleniumBase(object):
    def __init__(self,browser = 'web'):
        if browser == 'embed':
            self.service = webdriver.chrome.service.Service(executable_path='chromedriver.exe')
            self.service.start()
            chrome_options = Options()
            chrome_options.debugger_address = 'localhost:9222' #--remote-debugging-port=9222
            # chrome_options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
            capabilities = chrome_options.to_capabilities()
            self.driver = webdriver.Remote(command_executor=self.service.service_url, desired_capabilities=capabilities)
            assert 'Picasso' in self.driver.title, 'failed to attached to embedded page'
        else:
            self.driver = webdriver.Chrome()
            self.driver.get('http://vmsfgenuidev2/loanAdministration/positions')
            self.driver.maximize_window()
            self.driver.implicitly_wait(10)
            assert 'Picasso' in self.driver.title, 'failed to open page http://vmsfgenuidev2/loanAdministration/positions'

    def find_element(self,*element):
        try:
            WebDriverWait(self.driver,15).until(EC.visibility_of_all_elements_located(element))
            return self.driver.find_element(*element)
        except:
            print("cannot find page element: %s"%self,element)

    def find_elements(self,*element):
        try:
            WebDriverWait(self.driver,30).until(EC.visibility_of_all_elements_located(element))
            return self.driver.find_elements(*element)
        except:
            print("cannot find page element: %s"%self,element)

    def click(self,element):
        """click on element"""
        element = self.find_element(element)
        element.click()

    def send_keys(self,element,text):
        """send text"""
        element = self.find_element(element)
        element.clear()
        element.send_keys(text)

    def move_to_element(self, element):
        '''
        move mouse to element
        Usage:
        element = ("id","xxx")
        driver.move_to_element(element)
        '''
        element = self.find_element(element)
        ActionChains(self.driver).move_to_element(element).perform()

    def back(self):
        """
        back to preview browser
        """
        self.driver.back()

    def forward(self):
        """
        to next browser
        """
        self.driver.forward()

    def close(self):
        """
        close browser
        """
        self.driver.close()

    def quit(self):
        """
        quit browser
        """
        self.driver.quit()

    def get_title(self):
        '''get page title'''
        return self.driver.title

    def get_text(self, element):
        '''get text'''
        element = self.find_element(element)
        return element.text

    def get_attribute(self, element, name):
        '''get attribute'''
        element = self.find_element(element)
        return element.get_attribute(name)

    def js_execute(self, js):
        '''execute js'''
        return self.driver.execute_script(js)

    def js_focus_element(self, element):
        '''focus on element'''
        target = self.find_element(element)
        self.driver.execute_script("arguments[0].scrollIntoView();", target)

    def js_scroll_top(self):
        '''scroll up to the top'''
        js = "window.scrollTo(0,0)"
        self.driver.execute_script(js)

    def js_scroll_end(self):
        '''scroll down to the end'''
        js = "window.scrollTo(0,document.body.scrollHeight)"
        self.driver.execute_script(js)

    def select_by_index(self, element, index):
        '''select by index'''
        element = self.find_element(element)
        Select(element).select_by_index(index)

    def select_by_value(self, element, value):
        '''select by value'''
        element = self.find_element(element)
        Select(element).select_by_value(value)

    def select_by_text(self, element, text):
        '''select by text'''
        element = self.find_element(element)
        Select(element).select_by_value(text)

    def is_text_in_element(self,element,text,timeout=10):
        """if text is in element, focus on the element and return true, else return false"""
        try:
            result = WebDriverWait(self.driver,timeout,1).until(EC.text_to_be_present_in_element(element,text))
        except TimeoutException:
            print("cannot find element: "+str(element))
            return False
        else:
            return result

    def is_text_in_value(self,element,value,timeout = 10):
        '''
        if element value is in text, return result, else return false.
        result = driver.text_in_element(element, text)
        '''
        try:
            result = WebDriverWait(self.driver, timeout, 1).until(
                EC.text_to_be_present_in_element_value(element, value))
        except TimeoutException:
            print("cannot find element：" + str(element))
            return False
        else:
            return result

    def is_title(self, title, timeout=10):
        '''is title equal to?'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.title_is(title))
        return result

    def is_title_contains(self, title, timeout=10):
        '''is titile contain to?'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.title_contains(title))
        return result

    def is_selected(self, element, timeout=10):
        '''is element selected? return boolean'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.element_located_to_be_selected(element))
        return result

    def is_selected_be(self, element, selected=True, timeout=10):
        '''expected status of selected is True or False, return boolean'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.element_located_selection_state_to_be(element, selected))
        return result

    def is_alert_present(self, timeout=10):
        '''if alert presents, return alert, else return False'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.alert_is_present())
        return result

    def is_visibility(self, element, timeout=10):
        '''if element is visibility, return element, else return False'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.visibility_of_element_located(element))
        return result

    def is_invisibility(self, element, timeout=10):
        '''if element is invisibility, return element, else return False'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.invisibility_of_element_located(element))
        return result

    def is_clickable(self, element, timeout=10):
        '''if element is clickable, return element, else return False'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.element_to_be_clickable(element))
        return result

    def is_located(self, element, timeout=10):
        '''If element is located, return element, else return False'''
        result = WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located(element))
        return result