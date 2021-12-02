#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import calendar
from datetime import datetime

import dash_bootstrap_components as dbc
from dash import Dash, html, dcc

from hardio.dashapp import UserConfig
from iobrocker import IO
from .utils import CalendarFormatter
from ..presenter_config import AppDashIDs as ids, Buttons as btn


class AppCalendar:
    def __init__(self, io: IO, formatter: CalendarFormatter):
        self.io = io
        self.formatter = formatter

    def make_layout(self, context: dict = None) -> Dash.layout:
        if (not context) or ('month_year' not in context):
            month_year = None
        elif 'action' in context and context['action'] == 'refresh':
            month_year = context['month_year']
            self.refresh_activities_from_strava(month_year)
        else:
            month_year = context['month_year']
        return self.assemble_calendar(month_year)

    def assemble_calendar(self, month_year):
        month, year = self.set_month_year_based_on_user_pref_or_config(month_year)
        cal = calendar.Calendar().monthdatescalendar(year, month)
        activities_list = self.io.get_list_of_hardio_activities_in_range(cal[0][0], cal[-1][-1])
        formatted_cal = self.formatter.format_month(cal, activities_list)
        return self._make_layout(formatted_cal, month, year)

    def _make_layout(self, formatted_cal, month, year):
        calendar_table = self._make_card_table(formatted_cal)
        alert = self._make_alert()
        return html.Div(
            id="calendar",
            children=[html.Div(
                [
                    self.make_month_selector(month, year),
                    dbc.Button(btn.refresh_activities.name, id=btn.refresh_activities.id, n_clicks=0, color="link"),
                ],
                style={'width': '10rem'}),
                html.Br(),
                alert,
                html.Div(dbc.Spinner(html.Div(id="refresh_spinner"), size="sm")),
                calendar_table,
                dcc.Store(id="user_config_store", storage_type='session'),
            ]
        )

    def _make_alert(self):
        return html.Div(
            [
                dbc.Alert(
                    "Refresh may take up to a minute or so, depending on number of activities",
                    id=ids.calendar_refresh_alert,
                    is_open=False,
                    duration=4000,
                ),
            ]
        )

    def _make_card_table(self, formatted_cal: list[dict]) -> html.Div:
        cards = []
        for week in formatted_cal:
            week_cards = []
            for day, val in week.items():
                week_cards.append(self._make_card(day, val))
            cards.append(dbc.CardGroup(week_cards))
        return html.Div(cards)

    def _make_card(self, header: str, body: list, style: dict = None) -> dbc.Card:
        if style is None:
            style = {
                "width": "14rem",
                "font-size": "x-small",
            }
        card = dbc.Card(
            [
                dbc.CardHeader(header, style={"font-size": "smaller"}),
                dbc.CardBody(
                    [b for b in body]
                ),
            ],
            style
        )
        return card



    def make_month_selector(self, month: int, year: int) -> dbc.Select:
        earliest, _ = self.io.get_user_activity_date_range()
        _today = datetime.now()

        next_year = [_today.year + 1]
        next_months = [d for d in range(_today.month + 1, 13)][::-1]
        today = [_today.month]
        prev_months = [d for d in range(1, _today.month)][::-1]
        prev_years = list(range(earliest.year, _today.year))[::-1]

        selector = self._make_selector(
            {
                'next_year': next_year,
                'next_months': next_months,
                'today': today,
                'prev_months': prev_months,
                'prev_years': prev_years
            },
            month,
            year
        )
        return selector

    def _make_selector(self, options: dict, month: int, year: int) -> dbc.Select:
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

    def set_month_year_based_on_user_pref_or_config(self, user_selected_moth_year: str) -> tuple[int, int]:
        """
        Produce Month/Year combination to filter calendar by based on user preference (if provided)
        or based on UserConfig retrieved from db. Returns month/year values of today as a fallback
        :param user_selected_moth_year: string containing user-selected combination of Month/Year
        :return: tuple[int, int] Month, Year
        """
        config = self.io.read_user_config()
        if user_selected_moth_year:
            month_year = self._month_year_to_tuple(user_selected_moth_year)
            self.update_user_config_in_db(config, month_year)
            month, year = month_year
        elif config.user_calendar_date_preference:
            month, year = config.user_calendar_date_preference
        else:
            month: int = datetime.now().month
            year: int = datetime.now().year
        return month, year

    def update_user_config_in_db(self, config: UserConfig, month_year: tuple[int, int]) -> None:
        """
        Updates UserConfig based on latest calendar Month/Year view preference. Saves UserConfig to db
        :param config: instance of UserConfig
        :param month_year: tuple[int, int] Month, Year
        :return: None
        """
        config.user_calendar_date_preference = month_year
        self.io.save_user_config(config)

    def refresh_activities_from_strava(self, month_year: str) -> None:
        month, year = self._month_year_to_tuple(month_year)
        self.io.refresh_user_activities_from_strava(month, year)

    def _month_year_to_tuple(self, month_year: str) -> tuple[int, int]:  # Month, Year
        """
        Parses user-preferred combination of Month/Year string and returns tuple
        :param month_year: string Month/Year combination space separated (i.e. 10 2021)
        :return: tuple[int, int] Month, Year
        """
        m, y = month_year.split(" ")
        return int(m), int(y)  # Month, Year
