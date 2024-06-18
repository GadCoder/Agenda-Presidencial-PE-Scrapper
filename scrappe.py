import datetime
import requests

from selenium import webdriver
from bs4 import BeautifulSoup, NavigableString, Tag
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def find_iframe_source(soup: BeautifulSoup):
    iframe = soup.find_all('iframe')[0]
    try:
        src = iframe['src']
        return src
    except Exception as e:
        print(f"Error when finding iframe src: {e}")



def create_selenium_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--enable-javascript")
    return options

    options.add_argument('--headless')
    options.add_argument("--incognito")
    options.add_argument("--nogpu")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,1280")
    options.add_argument("--no-sandbox")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    return options


def create_selenium_driver():
    options = create_selenium_options()
    ua = UserAgent()
    userAgent = ua.random
    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": userAgent})
    return driver

def create_soup_from_source(url: str):
    driver = create_selenium_driver()
    driver.get(url)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'tab-controller-container-week'))
        )
        element.click()
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'tgTable'))
        )
        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")
        return soup
    finally:
        driver.quit()


def find_calendar_container(soup: BeautifulSoup):
    calendar_container = soup.find(id='tgTable')
    if calendar_container is None:
        print(f"Calendar container not founded")
    return calendar_container


def get_current_day() -> int:
    current_date = datetime.datetime.now()
    day_number = current_date.isoweekday()
    return day_number

def get_days_columns(container: Tag | NavigableString):
    days_columns = container.find_all(class_ = 'tg-col')
    current_day_column = container.find_all(class_ = 'tg-col-today')[0]
    current_day = get_current_day()
    current_day_position = current_day - 1
    days_columns.insert(current_day_position, current_day_column)
    return days_columns    


def get_activities_from_day(day: Tag | NavigableString):
    activities = day.find_all(class_ = 'chip-caption')
    activities = [activity.text for activity in activities]
    if len(activities) == 0:
        print("\t No hubieron actividades")
    for activity in activities:
        print(f"\t -{activity}")


def get_day_name(day_number: int) -> str:
    days = {
        1: "Lunes",
        2: "Martes",
        3: "Miercoles",
        4: "Jueves",
        5: "Viernes",
        6: "Sábado",
        7: "Domingo"
    } 
    return days[day_number]


def main():
    url = 'https://www.gob.pe/institucion/presidencia/agenda'
    request = requests.get(url=url)
    soup = BeautifulSoup(request.text, features='html.parser')
    iframe_source = find_iframe_source(soup=soup)
    calendar_soup = create_soup_from_source(url=iframe_source)
    calendar_container = find_calendar_container(soup=calendar_soup)
    days = get_days_columns(container=calendar_container)
    for i, day in enumerate(days):
        day_name = get_day_name(i + 1)
        print(f"{day_name.upper()}: ")
        get_activities_from_day(day=day)


if __name__ == "__main__":
    main()