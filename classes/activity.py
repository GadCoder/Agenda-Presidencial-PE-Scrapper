from datetime import datetime
from bs4 import NavigableString, Tag

class Activity:
    def __init__(self, container: Tag | NavigableString, day: int, month: int, year: int) -> None:
        self.activity_date: datetime = None
        self.description: str = ""
        self.location: str = ""

        self.create(container=container, day=day, month=month, year=year)
    

    def create(self, container: Tag | NavigableString, day: int, month: int, year: int):
        spans = container.find_all('span')
        if len(spans) == 1:
            activity_text = spans[0].text
        elif len(spans) == 2:
            """
            The character U+2013 "–" could be confused with the ASCII character U+002d "-",
            which is more common in source code
            Gracias Google
            """
            hour = spans[0].text.split("–")[0].strip()
            description = spans[-1].text
            activity_text = f"{hour} - {description}"

        self.get_info_from_activity(activity_text=activity_text, day=day, month=month, year=year)


    def get_info_from_activity(self, activity_text: str, day: int, month: int, year: int):
        hour, minutes = self.get_hour_and_minutes_from_text(activity_text=activity_text)
        self.activity_date = datetime(day=day, month=month, hour=int(hour), minute=int(minutes), year=year).isoformat()
        self.get_description_and_location_from_text(activity_text=activity_text)


    def get_hour_and_minutes_from_text(self, activity_text: str):
        parts = activity_text.split("-")
        hour, minutes = parts[0].strip().split(":")
        return int(hour), int(minutes)
    

    def get_description_and_location_from_text(self, activity_text: str):
        parts = activity_text.split("-")
        if len(parts) > 2:
            description = " ".join(parts[1:])
        else:
            description = parts[1]
        activity = description
        location = ""
        repetitions_of_lugar = description.count("Lugar")
        if repetitions_of_lugar != 0:
            if repetitions_of_lugar > 1:
                parts = description.split("Lugar:")
                activity = parts[0]
                location = parts[-1]
            else:
                activity, location = description.split("Lugar:")
        self.description = activity.strip()
        self.location = location.strip()   


    def export_activity(self):
        return (self.description, self.location, self.activity_date)
