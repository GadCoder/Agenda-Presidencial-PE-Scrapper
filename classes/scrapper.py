import requests
from time import sleep

import pandas as pd
from bs4 import BeautifulSoup

from classes.selenium_driver import SeleniumDriver
from classes.calendar_week import CalendarWeek

class Scrapper:
    def __init__(self) -> None:
        self.iframe_src: str | None = None
        self.soup: BeautifulSoup = None
        self.selenium_driver: SeleniumDriver = SeleniumDriver()
        self.calendar_weeks: list[CalendarWeek] = []
        
        self.get_iframe_link()
        self.selenium_driver.start()
        self.create_soup()


    def create_soup(self):
        try:
            html = self.selenium_driver.get_current_week_page(url=self.iframe_src)
            soup = BeautifulSoup(html, features="html.parser")
            self.soup = soup
        except Exception as e:
            print(f"Error creating soup -> {e}")

    
    def get_iframe_link(self):
        url = 'https://www.gob.pe/institucion/presidencia/agenda'
        request = requests.get(url=url)
        soup = BeautifulSoup(request.text, features='html.parser')
        iframe = soup.find('iframe')
        try:
            src = iframe['src']
            self.iframe_src = src
        except Exception as e:
            print(f"Error when finding iframe src: {e}")
      

    def get_current_activities(self):
        try:
            current_week = CalendarWeek(soup=self.soup)
            current_week.show_activities()
            self.calendar_weeks.append(current_week)
        finally:
            self.selenium_driver.kill_driver()


    def is_on_last_week(self, week: CalendarWeek,  day: int, month: int, year: int):
        if week.year < year:
            return True
        week_month = week.calendar_days[0].month
        if week_month < month:
            return True
        for calendar_day in week.calendar_days:
            if calendar_day.day <= day and week_month == month:
                return True
        return False


    def get_history_data(self, last_day: int, last_month: int, last_year: int):
        try:    
            soup = self.soup
            while True:
                week = CalendarWeek(soup=soup)
                week.show_activities()
                self.calendar_weeks.append(week)
                is_on_last_week = self.is_on_last_week(week=week, day=last_day, month=last_month, year=last_year)
                if is_on_last_week:
                    return
                sleep(5)
                html = self.selenium_driver.get_previous_week_page()
                soup = BeautifulSoup(html, features="html.parser")
        finally:
            self.selenium_driver.kill_driver()


    def export_data_to_csv(self):
        activities = []
        for calendar_week in self.calendar_weeks:
            for day in calendar_week.calendar_days:
                for activity in day.activities:
                    activities.append(activity.export_activity())
        df = pd.DataFrame(activities)
        df.columns = ['activity', 'place', 'datetime']
        print(f"{len(activities)} activities imported to activities.csv")
        df.to_csv('activities.csv', index=True)