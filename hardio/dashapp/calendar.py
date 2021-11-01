#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import calendar
from datetime import datetime

from dash import Dash, dash_table, html
import dash_bootstrap_components as dbc

from hardio.dashapp import UserConfig
from iobrocker import IO
from logic import Activity, PresentationActivity

WEEK_DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


class HardioCalendar(calendar.Calendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super().__init__()

    def format_month(self, month: list[list[datetime.date]], activities: list[PresentationActivity]):
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


def _make_selector(options: dict, month: int, year: int) -> dbc.Select:
    _this_year = datetime.now().year
    c = calendar.month_name

    next_year = [{"label": options['next_year'], "value": f"1 {options['next_year'][0]}"}]  # Jan (1) Year
    next_months = [{"label": f"{c[m]} {_this_year}", "value": f"{m} {_this_year}"} for m in
                   options['next_months']]  # Months Year
    today = [{"label": "Today", "value": f"{options['today'][0]} {_this_year}", 'active': True}]  # Month Year
    prev_months = [{"label": f"{c[m]} {_this_year}", "value": f"{m} {_this_year}"} for m in
                   options['prev_months']]  # Months Year
    prev_years = [{"label": y, "value": f"1 {y}"} for y in options['prev_years']]  # Jan (1) Year

    selector = dbc.Select(
        id="calendar_month_selector",
        placeholder=f"{c[month]}, {year}",
        options=(next_year + next_months + today + prev_months + prev_years),
        persistence=True,
    )
    return selector


def make_month_selector(user_id: int, year: int, month: int) -> dbc.Select:
    earliest, _ = IO(user_id).get_user_activity_date_range()
    _today = datetime.now()

    next_year = [_today.year + 1]
    next_months = [d for d in range(_today.month + 1, 13)][::-1]
    today = [_today.month]
    prev_months = [d for d in range(1, _today.month)][::-1]
    prev_years = list(range(earliest.year, _today.year))[::-1]

    selector = _make_selector(
        {
            'next_year': next_year,
            'next_months': next_months,
            'today': today,
            'prev_months': prev_months,
            'prev_years': prev_years
        },
        year,
        month
    )
    return selector


def make_layout(user_id: int, user_selected_moth_year: str = None) -> Dash.layout:
    io = IO(user_id)
    month, year = set_month_year(io, user_selected_moth_year)

    cal = calendar.Calendar().monthdatescalendar(year, month)
    activities_list = io.get_list_of_hardio_activities_in_range(cal[0][0], cal[-1][-1])
    formatted_cal = HardioCalendar().format_month(cal, activities_list)

    columns = [{'id': d,
                'name': d,
                'editable': False,
                'type': 'text',
                'presentation': 'markdown',
                }
               for d in WEEK_DAYS]

    table = dash_table.DataTable(
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
            {
                "selector": "dash-spreadsheet-container dash-spreadsheet dash-virtualized dash-freeze-top dash-no-filter dash-fill-width",
                "rule": "max-height: 1200px; height: 1200px"},
            # {"selector": ".dash-table-container tr", "rule": 'max-height: "150px"; height: "150px"; '},
            # {"selector": "dash-spreadsheet dash-freeze-top dash-spreadsheet dash-virtualized", "rule": "max-height: inherit !important;"},
            # {"selector": "dash-table-container", "rule": "max-height: calc(100vh - 225px);"}

        ],
    )

    alert = html.Div(
        [
            dbc.Alert(
                "Refresh may take up to a minute or so, depending on number of activities",
                id="alert-calendar-refresh",
                is_open=False,
                duration=4000,
            ),
        ]
    )

    layout = html.Div(
        id="calendar_view",
        children=[
            html.Div(
                [
                    make_month_selector(user_id, month, year),
                    dbc.Button('Refresh', id='btn_refresh_activities', n_clicks=0, color="link"),
                ],
                style={'width': '10rem'}),
            html.Br(),
            alert,
            dbc.Spinner(html.Div(id="refresh_spinner",
                                 children='calendar')),
            table
        ]
    )

    return layout


def set_month_year(io: IO, user_selected_moth_year: str) -> tuple[int, int]:
    """
    Produce Month/Year combination to filter calendar by
    :param io: instance of IO object
    :param user_selected_moth_year: string containing user-selected combination of Month/Year
    :return: tuple[int, int] Month, Year
    """
    config = io.read_user_config()
    if user_selected_moth_year:
        month_year = _month_year_to_tuple(user_selected_moth_year)
        update_user_config_in_db(config, io, month_year)
        month, year = month_year
    elif config.user_calendar_date_preference:
        month, year = config.user_calendar_date_preference
    else:
        month: int = datetime.now().month
        year: int = datetime.now().year
    return month, year


def update_user_config_in_db(config: UserConfig, io: IO, month_year: tuple[int, int]) -> None:
    """
    Updates UserConfig based on latest calendar Month/Year view preference. Saves UserConfig to db
    :param config: instance of UserConfig
    :param io: instance of IO object
    :param month_year: tuple[int, int] Month, Year
    :return: None
    """
    config.user_calendar_date_preference = month_year
    io.save_user_config(config)


def refresh_activities_from_strava(user_id: int, month_year: str) -> None:
    month, year = _month_year_to_tuple(month_year)
    io = IO(user_id)
    io.refresh_user_activities_from_strava(month, year)


def _month_year_to_tuple(month_year: str) -> tuple[int, int]:  # Month, Year
    """
    Parses user-preferred combination of Month/Year string and returns tuple
    :param month_year: string Month/Year combination space separated (i.e. 10 2021)
    :return: tuple[int, int] Month, Year
    """
    m, y = month_year.split(" ")
    return int(m), int(y)  # Month, Year
