#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import calendar
from datetime import datetime

from dash_table import DataTable

from iobrocker import IO
from middleware import Activity, PresentationActivity

WEEK_DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
WEEK_DAYS_DICT = {'Mon': 0, 'Tue': 1, 'Wed': 2, 'Thu': 3, 'Fri': 4, 'Sat': 5, 'Sun': 6}


def day_of_week_to_str(day_of_week: int) -> str:
    return WEEK_DAYS[day_of_week]


def datetime_to_monthdate(dt):
    return dt.strftime("%b, %d")


def get_month_template(year: int, month: int):
    days = [d for d in calendar.Calendar(calendar.firstweekday()).itermonthdates(year, month)]
    return [({day_of_week_to_str(d.weekday()): datetime_to_monthdate(d) for d in days[i:i + 7]}) for i in
            range(0, len(days), 7)]


# layout = DataTable(
#     id="calendar",
#     data=get_month_template(datetime.now().year, datetime.now().month),
#     columns=[{'id': d, 'name': d} for d in WEEK_DAYS],
#     page_size=3,
#     page_current=0,
#     virtualization=True,
#     fixed_rows={'headers': True},
#     style_cell={'minWidth': 95, 'width': 95, 'maxWidth': 95},
#     style_table={'height': 300},  # default is 500,
# )


class HardioCalendar(calendar.Calendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super().__init__()

    def format_day(self, day: datetime.date, activities: list[PresentationActivity]):
        if day != 0:
            activities_of_day = list(filter(lambda x: x.date.date() == day, activities))
            d = f"{day.day}"
            if activities_of_day:
                links = []
                for activity in activities_of_day:
                    links.append(f"[{activity.name}](/application/activity/{activity.id})")
                d = links
            return d
        return {}

    def format_week(self, week: list[datetime.date], activities: list[PresentationActivity]):
        w = {}
        for day in week:
            w[day_of_week_to_str(day.weekday())] = self.format_day(day, activities)
        return w

    def format_month(self, month: list[list[datetime.date]], activities: list[PresentationActivity]):
        m = []
        for week in month:
            m.append(self.format_week(week, activities))
        return m


def make_layout(user_id):
    cal = calendar.Calendar().monthdatescalendar(2021, 8)
    io = IO(user_id)
    activities_list = io.get_list_of_activities_in_range(cal[0][0], cal[-1][-1])
    formatted_cal = HardioCalendar().format_month(cal, activities_list)

    # columns = [
    #     {'name': 'Mon', 'id': 'Mon', 'type': 'datetime', 'editable': False, 'presentation': 'markdown'},
    #     {'name': 'Tue', 'id': 'Tue', 'type': 'datetime', 'editable': False, 'presentation': 'markdown'},
    #     {'name': 'Wed', 'id': 'Mon', 'type': 'datetime', 'editable': False, 'presentation': 'markdown'},
    #     {'name': 'Thu', 'id': 'Thu', 'type': 'datetime', 'editable': False, 'presentation': 'markdown'},
    #     {'name': 'Fri', 'id': 'Fri', 'type': 'datetime', 'editable': False, 'presentation': 'markdown'},
    #     {'name': 'Sat', 'id': 'Sat', 'type': 'datetime', 'editable': False, 'presentation': 'markdown'},
    #     {'name': 'Sun', 'id': 'Sun', 'type': 'datetime', 'editable': False, 'presentation': 'markdown'},
    # ]

    columns = [{'id': d,
                'name': d,
                'editable': False,
                'type': 'text',
                'presentation': 'markdown',
                }
               for d in WEEK_DAYS]

    layout = DataTable(
        id="calendar",
        data=formatted_cal,
        columns=columns,
        # page_size=3,
        # page_current=0,
        virtualization=True,
        fixed_rows={'headers': True},
        style_cell={'minWidth': 95, 'width': 95, 'maxWidth': 95, 'minHeight': 95},
        style_table={'height': 500},  # default is 500,
        markdown_options={"link_target": "_self"},
        css=[
            {"selector": ".dash-spreadsheet tr th", "rule": "height: 15px;"},  # set height of header
            {"selector": ".dash-spreadsheet tr td", "rule": "height: 75px;"},  # set height of body rows
        ]
    )

    return layout
