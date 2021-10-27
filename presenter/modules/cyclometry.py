#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
from __future__ import annotations

import gzip
import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

from .utils.cyclometry_drawer import CyclometryDrawer


@dataclass
class CActivity:
    """
    Represents Cyclometry Activity
    """

    activity_json: dict
    samples_key: str = 'samples'
    time_key: str = 'secs'
    df: pd.DataFrame = pd.DataFrame()

    athlete: Optional[str] = None
    avgHr: Optional[int] = None
    avgPower: Optional[int] = None
    awc: Optional[int] = None
    awcMinValue: Optional[int] = None
    awcs: Optional[float] = None
    calendarText: Optional[str] = None
    cho: Optional[int] = None
    cp: Optional[int] = None
    cps: Optional[float] = None
    data: Optional[str] = None
    device: Optional[str] = None
    deviceInfo: Optional[str] = None
    devicetype: Optional[str] = None
    fat: Optional[int] = None
    fileFormat: Optional[str] = None
    filename: Optional[str] = None
    gp: Optional[int] = None
    gps: Optional[float] = None
    id: Optional[int] = None
    identifier: Optional[str] = None
    maxHr: Optional[int] = None
    maxPower: Optional[int] = None
    notes: Optional[str] = None
    objective: Optional[str] = None
    recintsecs: Optional[int] = None
    secBelowZeroAwc: Optional[int] = None
    secBelowZeroSwc: Optional[int] = None
    sport: Optional[str] = None
    starttime: Optional[str] = None
    swc: Optional[int] = None
    swcMinValue: Optional[int] = None
    swcs: Optional[float] = None
    weekday: Optional[str] = None
    workoutCode: Optional[str] = None
    year: Optional[str] = None

    def __post_init__(self):
        self.df = self.samples_to_df(self.activity_json[self.samples_key])
        self.populate_fields()

    def samples_to_df(self, samples):
        return pd.DataFrame(samples)

    def populate_fields(self):
        for field_name, value in self.activity_json.items():
            if field_name != 'samples_key':
                self.__setattr__(field_name, value)

    def get_activity_date_time(self):
        try:
            return datetime.strptime(self.starttime, '%Y/%m/%d %H:%M:%S %Z')
        except ValueError as e:
            return self._derive_starttime_from_identifier()

    def _derive_starttime_from_identifier(self):
        date = self.identifier.split(': ')[-1]
        return datetime.strptime(date, '%d.%m.%Y')

    def normalize_samples(self, samples):
        for s, i in zip(samples, range(len(samples))):
            s['SECS'] = i
        return samples

    def _list_json_fields(self):
        s = "\'\'"
        for k, v in self.activity_json.items():
            if k != 'samples':
                type_string = {type(v).__name__}
                print(f"{k}: Optional[{type_string}] = None")

    def get_activity_date_string(self):
        return self.get_activity_date_time().strftime('%b %d, %Y')

    def get_activity_duration(self):
        return timedelta(seconds=int(self.df[self.time_key].max()))

    def get_total_work(self):
        return self.df['totalWork'].max()

    @classmethod
    def from_file(cls, path: str) -> CActivity:
        with gzip.open(path, 'r') as f:
            return cls(json.load(f))


class Cyclometry:

    def make_layout(self):
        layout = dbc.Card(dbc.CardBody(
            [
                html.Div(
                    [
                        self.make_cyclometry_page()
                    ]
                )
            ]
        ), className="mt-3")
        return layout

    def make_cyclometry_page(self):
        c_activity = self.get_c_activity()
        header = self.make_header(c_activity)
        fig = self.make_fig(c_activity)
        page = html.Div(
            [
                header,
                html.Br(),
                dcc.Graph(id='cyclometry_chart', figure=fig)
            ]
        )
        return page

    def get_c_activity(self, activity_id: int = None) -> CActivity:
        return CActivity.from_file('temp/2021-10-21_10-16-41.json')

    def make_header(self, c_activity: CActivity) -> html.Div:
        elements = [
            f"Activity: {c_activity.identifier}",
            f"Date: {c_activity.get_activity_date_string()}",
            f"Duration: {c_activity.get_activity_duration()}",
            f"AVG Power: {c_activity.avgPower} W",
            f"MAX Power: {c_activity.maxPower} W",
            f"AVG HR: {c_activity.avgHr} bpm",
            f"MAX HR: {c_activity.maxHr} bpm",
            f"AWC below Zero: {c_activity.secBelowZeroAwc}s | {c_activity.awcMinValue}J",
            f"SWC below Zero: {c_activity.secBelowZeroSwc}s | {c_activity.swcMinValue}J",
            f"CP and AWC Stress: {c_activity.cps} - {c_activity.awcs}",
            f"GP and SWC Stress: {c_activity.gps} - {c_activity.swcs}",
            f"Total Work: {c_activity.get_total_work()} J",
            f"CH and Fat: {c_activity.cho}g {c_activity.fat}g",
        ]
        first_row = html.H6(elements[0])  # style={'font-size': '0.7rem'}),

        header = html.Div(
            [
                first_row,
                self.make_row(self.make_cards(elements)),
            ],
            style={'font-size': '0.7rem'}
        )
        return header

    def make_cards(self, elements: list) -> list[dbc.Card]:
        cards = []

        it = iter(elements[1:])
        pairs = list(zip(it, it))
        for pair in pairs:
            card = dbc.Card(
                dbc.CardBody(
                    [
                        html.P(pair[0], className="card-text"),
                        html.P(pair[1], className="card-text"),
                    ]
                )
            )
            cards.append(card)
        return cards

    def make_row(self, cards: list[dbc.Card]):
        row = [dbc.Col(card, width='auto') for card in cards]
        return dbc.Row(row, no_gutters=True)

    def make_fig(self, c_activity) -> CyclometryDrawer.get_fig:
        drawer = CyclometryDrawer(df=c_activity.df, index_col='secs',
                                  series_to_plot=[s for s in c_activity.df.columns if s != 'secs'])
        fig = drawer.get_fig()
        return fig
