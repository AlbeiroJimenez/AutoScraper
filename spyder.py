from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import *

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'

class Spyder:
    def __init__(self):
        self.driver = None
        self.url    = None
        self.set    = True
        
    def getDriver(self):
        return self.driver
        
    def getUrl(self):
        return self.url
    
    def setDriver(self, url):
        if self.set:
            self.driver = self.setHeadlessMode()
            self.set    = False
        self.driver.maximize_window()
        self.setUrl(url)
        self.loadPage()
        
    def setUrl(self, url):
        self.url = url
        
    def loadPage(self, url = None):
        if url == None:
            url = self.url
        self.driver.get(url)
        
    def setHeadlessMode(self):
        fireFoxOptions = webdriver.FirefoxOptions()
        #fireFoxOptions.headless = True
        fireFoxOptions.set_preference("general.useragent.override", USER_AGENT)
        #fireFoxOptions.page_load_strategy = 'eager'
        service = FirefoxService(executable_path=GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options = fireFoxOptions)
    
    def getWebElement(self, typeSearch, expression, timeout_=3, max_iteractions=6, visible = True, driver = None):
        flat = 0
        while flat<max_iteractions:
            if typeSearch=='XPATH' and visible:
                try:
                    if driver == None:
                        webElement = WebDriverWait(self.driver, timeout_).until(EC.visibility_of_any_elements_located((By.XPATH, expression)))
                    else:
                        webElement = WebDriverWait(driver, timeout_).until(EC.visibility_of_any_elements_located((By.XPATH, expression)))
                    return webElement, None
                except TimeoutException as e:
                    flat += 1
                    if flat>=max_iteractions:
                        return -1, e
                except InvalidSelectorException as e:
                    return -1, e
                except:
                    return -1, sys.exc_info()
            elif typeSearch=='XPATH' and  not visible:
                try:
                    while flat<max_iteractions:
                        time.sleep(1)
                        if driver == None:
                            webElement = self.driver.find_elements(By.XPATH, expression)
                        else:
                            webElement = driver.find_elements(By.XPATH, expression)
                        if len(webElement)>0:
                            return webElement, None
                        flat += 1
                    else:
                        return -1, None
                except InvalidSelectorException as e:
                    return -1, e
                except:
                    return -1, sys.exc_info()
            elif typeSearch == 'TAG_NAME':
                pass
            elif typeSearch == 'CLASS':
                pass
        return -1, None
    
    def existWebElement(self, typeSearch, expression, driver=None):
        if typeSearch == 'XPATH':
            try:
                if driver == None:
                    WebDriverWait(self.driver, 10).until(EC.visibility_of_any_elements_located((By.XPATH, expression)))
                else:
                    WebDriverWait(driver, 10).until(EC.visibility_of_any_elements_located((By.XPATH, expression)))
                return True
            except:
                return False
            
    def scrollDown(self):
        self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            
if __name__ == '__main__':
    spyder = Spyder()   