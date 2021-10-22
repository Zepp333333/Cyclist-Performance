#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import calendar
from datetime import datetime
from logic import PresentationActivity

WEEK_DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


class CalendarFormatter:
    """
    Utility class contains set of methods that produce formatted calendar for provided month and a list
    of PresentationActivity-es.
    """

    def __call__(self, month: calendar.Calendar().monthdatescalendar, activities: list[PresentationActivity]):
        """
        Produce a formatted calendar.
        :param month: calendar.Calendar().monthdatescalendar
        :param activities: list of PresentationActivity for the same time-range as month param
        """
        return self.format_month(month, activities)

    def format_month(self, month: calendar.Calendar().monthdatescalendar, activities: list[PresentationActivity]):
        m = []
        for week in month:
            m.append(self.format_week(week, activities))
        return m

    def format_week(self, week: list[datetime.date], activities: list[PresentationActivity]):
        w = {}
        for day in week:
            w[self.day_of_week_to_str(day.weekday())] = self.format_day(day, activities)
        return w

    def format_day(self, day: datetime.date, activities: list[PresentationActivity]):
        if day == 0:
            return {}
        activities_of_day = list(filter(lambda x: x.date.date() == day, activities))
        d = f"{day.day}"
        if activities_of_day:
            links = []
            for activity in activities_of_day:
                links.append(f"[{activity.name}](/application/activity/{activity.id}) \n")
            d = links
        return d

    def day_of_week_to_str(self, day_of_week: int) -> str:
        return WEEK_DAYS[day_of_week]
