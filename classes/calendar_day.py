from typing import Any
from bs4 import NavigableString, ResultSet, Tag
from classes.activity import Activity

class CalendarDay:
    def __init__(self, header: str, day_column: Tag | NavigableString, year: int) -> None:
        self.day: int = None
        self.month: int = None
        self.year: int = year
        self.activities: list[Activity] = []

        self.create(header=header, day_column=day_column)

    
    def create(self, header: str, day_column: Tag | NavigableString):
        day, month = header.split(" ")[-1].split("/")
        self.day = int(day)
        self.month = int(month)
        self.get_activities_from_day(day=day_column)


    def get_activities_from_day(self, day: Tag | NavigableString) -> list[str] | None:
        activities_containers = day.find_all('dl', class_='cbrd')
        if not activities_containers:
            return 
        for container in activities_containers:
            activity = Activity(container=container, day=self.day, month=self.month, year=self.year)
            self.activities.append(activity)


    def show_activities(self):
        print(f"{self.day}/{self.month}:")
        for activity in self.activities:
            print(f"\t-{activity.description}")