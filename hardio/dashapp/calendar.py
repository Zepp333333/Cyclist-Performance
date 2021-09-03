#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import calendar
from datetime import datetime

from dash_table import DataTable

from iobrocker import IO
from logic import Activity, PresentationActivity

WEEK_DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


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
                    links.append(f"[{activity.name}](/application/activity/{activity.id}) \n")
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


def day_of_week_to_str(day_of_week: int) -> str:
    return WEEK_DAYS[day_of_week]


def make_layout(user_id):
    cal = calendar.Calendar().monthdatescalendar(2021, 8)
    io = IO(user_id)
    activities_list = io.get_list_of_activities_in_range(cal[0][0], cal[-1][-1])
    formatted_cal = HardioCalendar().format_month(cal, activities_list)

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
        # virtualization=True,
        fixed_rows={'headers': True, 'data': 0},
        style_cell={
            'minWidth': 95,
            'width': 95,
            'maxWidth': 95,
        },
        style_data={
            'font_family': 'cursive',
            'font_size': '10px',
            'text_align': 'center',
            'white-space': 'normal',
            'height': 'auto',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'maxWidth': 0,
        },
        # style_table={'height': '500px'},  # default is 500,
        # style_table={
        #     'minHeight': '100vh', 'height': '100vh', 'maxHeight': '100vh',
        #     'minWidth': '900px', 'width': '900px', 'maxWidth': '900px'
        # },
        markdown_options={"link_target": "_self"},
        css=[
            {"selector": ".dash-spreadsheet tr th", "rule": "height: 15px;"},  # set height of header
            # {"selector": ".dash-spreadsheet tr td", "rule": "height: 75px;"},  # set height of body rows
            # {"selector": ".dash-spreadsheet-container", "rule": "max-height: 1000px;"},
            # {"selector": "table", "rule": "width: 100%;"},
            # {"selector": "cell cell-1-1 dash-fixed-content", "rule": "height: 100px;"},
            {"selector": "dash-spreadsheet-container dash-spreadsheet dash-virtualized dash-freeze-top dash-no-filter dash-fill-width", "rule": "max-height: 1200px; height: 1200px"},
            # {"selector": ".dash-table-container tr", "rule": 'max-height: "150px"; height: "150px"; '},
            # {"selector": "dash-spreadsheet dash-freeze-top dash-spreadsheet dash-virtualized", "rule": "max-height: inherit !important;"},
            # {"selector": "dash-table-container", "rule": "max-height: calc(100vh - 225px);"}

        ],
    )

    return layout
