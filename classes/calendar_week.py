

from datetime import datetime
from typing import Any
from bs4 import BeautifulSoup, NavigableString, ResultSet, Tag

from classes.calendar_day import CalendarDay


class CalendarWeek:
    def __init__(self, soup: BeautifulSoup) -> None:
        self.soup: BeautifulSoup = soup
        self.calendar_container: Tag | NavigableString | None = None
        self.days_headers: list[str] = None
        self.days_columns: ResultSet[Any] | Any = Any
        self.calendar_days: list[CalendarDay] = []
        self.month: int = None
        self.year: int = None

        self.create()


    def create(self):
        self.get_days_headers()
        self.get_calendar_container()
        self.get_week_year()
        self.get_calendar_days()


    def get_days_headers(self):
        headers_container = self.soup.find(id='topcontainer1')
        headers_elements = headers_container.find(class_='wk-daynames').find_all(class_='wk-dayname')
        day_headers = [header.span.text for header in headers_elements]
        self.days_headers = day_headers


    def get_calendar_container(self):
        calendar_container = self.soup.find(id='tgTable')
        if calendar_container is None:
            print(f"Calendar container not founded")
        self.calendar_container = calendar_container

    def get_current_day(self) -> int:
        current_date = datetime.now()
        day_number = current_date.isoweekday()
        return day_number


    def append_current_day(self, days_columns: ResultSet[Any] | Any, current_day_column: ResultSet[Any] | Any):
        current_day = self.get_current_day()
        current_day_position = current_day - 1
        days_columns.insert(current_day_position, current_day_column)


    def get_week_year(self) -> int:
        date_container = self.soup.find(id='currentDate1')
        parts = date_container.text.split()
        year = int(parts[-1].strip())
        self.year = year


    def get_calendar_days(self):
        days_columns = self.calendar_container.find_all(class_ = 'tg-col')
        current_day_column = self.calendar_container.find_all(class_ = 'tg-col-today')
        if current_day_column:
            current_day_column = current_day_column[0]
            self.append_current_day(days_columns=days_columns, current_day_column=current_day_column)
        for (header, day_column) in zip(self.days_headers, days_columns):
            calendar_day = CalendarDay(header=header, day_column=day_column, year=self.year)
            self.calendar_days.append(calendar_day)


    def show_activities(self):
        for calendar_day in reversed(self.calendar_days):
            calendar_day.show_activities()
