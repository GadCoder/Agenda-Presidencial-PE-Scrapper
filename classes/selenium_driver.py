from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SeleniumDriver:
    def __init__(self) -> None:
        self.driver: webdriver = None


    def start(self):
        self.create_selenium_driver()


    def create_selenium_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--enable-javascript")
        options.add_experimental_option('prefs', {'intl.accept_languages': 'en'})
        return options


    def create_selenium_driver(self):
        options = self.create_selenium_options()
        ua = UserAgent()
        userAgent = ua.random
        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": userAgent})
        self.driver = driver


    def get_current_week_page(self, url: str):
        self.driver.get(url)
        element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'tab-controller-container-week'))
        )
        element.click()
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'tgTable'))
        )
        return self.driver.page_source
    
    
    def get_previous_week_page(self):
        element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'tab-controller-container-week'))
            )
        element.click()
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'tgTable'))
        )
        previous_button = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'navBack1'))
        )
        previous_button.click()
        html = self.driver.page_source
        return html


    def kill_driver(self):
        self.driver.quit()
         