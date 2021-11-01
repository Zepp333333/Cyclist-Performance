#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
from __future__ import annotations

import gzip
import json
from datetime import datetime, timedelta
from typing import List

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from pydantic import BaseModel

from iobrocker import IO
from .utils.cyclometry_drawer import CyclometryDrawer


class Sample(BaseModel):
    awcstate: int
    cad: int
    hr: int
    pressure: int
    secs: int
    swcstate: int
    totalWork: int
    watts: int


class Model(BaseModel):
    """
    Pydantic model for Json. To rebuild:
    pip install datamodel-code-generator
    datamodel-codegen  --input <filename.json> --input-file-type json --output model.py

    """

    athlete: str
    avgHr: int
    avgPower: int
    awc: int
    awcMinValue: int
    awcs: float
    calendarText: str
    cho: int
    cp: int
    cps: float
    data: str
    device: str
    deviceInfo: str
    devicetype: str
    fat: int
    fileFormat: str
    filename: str
    gp: int
    gps: float
    id: int
    identifier: str
    maxHr: int
    maxPower: int
    notes: str
    objective: str
    recintsecs: int
    samples: List[Sample]
    secBelowZeroAwc: int
    secBelowZeroSwc: int
    sport: str
    starttime: str
    swc: int
    swcMinValue: int
    swcs: float
    weekday: str
    workoutCode: str
    year: str

class CActivity(Model):
    """
    Represents Cyclometry Activity
    """

    class Config:
        extra = 'allow'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.df = self.samples_to_df(self.samples)

    def samples_to_df(self, samples):
        flat_samples = [d.__dict__ for d in samples]
        return pd.DataFrame(flat_samples)

    @property
    def date(self):
        return self._get_activity_date_time().strftime('%b %d, %Y')

    @property
    def duration(self):
        return timedelta(seconds=int(self.df['secs'].max()))

    @property
    def total_work(self):
        return self.df['totalWork'].max()

    def _get_activity_date_time(self):
        try:
            return datetime.strptime(self.starttime, '%Y/%m/%d %H:%M:%S %Z')
        except ValueError as e:
            return self._derive_starttime_from_identifier()

    def _derive_starttime_from_identifier(self):
        date = self.identifier.split(': ')[-1]
        return datetime.strptime(date, '%d.%m.%Y')

    def _normalize_samples(self, samples):
        for s, i in zip(samples, range(len(samples))):
            s['SECS'] = i
        return samples



    @classmethod
    def from_file(cls, path: str) -> CActivity:
        with gzip.open(path, 'r') as f:
            return cls(**json.load(f))


class Cyclometry:

    def __init__(self, io: IO, context: dict) -> None:
        self.io = io
        self.context = context

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
        config_offcanvas = self.make_cyclometry_config(c_activity)
        fig = self.make_fig(c_activity)
        page = html.Div(
            [
                header,
                config_offcanvas,
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
            f"Date: {c_activity.date}",
            f"Duration: {c_activity.duration}",
            f"AVG Power: {c_activity.avgPower} W",
            f"MAX Power: {c_activity.maxPower} W",
            f"AVG HR: {c_activity.avgHr} bpm",
            f"MAX HR: {c_activity.maxHr} bpm",
            f"AWC below Zero: {c_activity.secBelowZeroAwc}s | {c_activity.awcMinValue}J",
            f"SWC below Zero: {c_activity.secBelowZeroSwc}s | {c_activity.swcMinValue}J",
            f"CP and AWC Stress: {c_activity.cps} - {c_activity.awcs}",
            f"GP and SWC Stress: {c_activity.gps} - {c_activity.swcs}",
            f"Total Work: {c_activity.total_work} J",
            f"CH and Fat: {c_activity.cho}g {c_activity.fat}g",
        ]
        first_row = html.H6(elements[0])  # style={'font-size': '0.7rem'}),

        header = html.Div(
            [
                first_row,
                self.make_row(self.make_cards(elements[1:])),
            ],
            style={'font-size': '0.7rem'}
        )
        return header

    def make_cards(self, elements: list) -> list[dbc.Card]:
        cards = []

        it = iter(elements)
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
        return dbc.Row(row, className="g-0")

    def make_fig(self, c_activity) -> CyclometryDrawer.get_fig:
        drawer = CyclometryDrawer(df=c_activity.df, index_col='secs',
                                  series_to_plot=[s for s in c_activity.df.columns if s != 'secs'])
        fig = drawer.get_fig()
        return fig

    def make_cyclometry_config(self, c_activity: CActivity) -> html.Div:
        config_view = html.Div(
            [
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H6(f"CP {c_activity.cp} W" ,className="card-text"),
                            html.H6(f"GP {c_activity.gp} W" ,className="card-text"),
                            html.H6(f"AWC {c_activity.awc} J" ,className="card-text"),
                            html.H6(f"SWC {c_activity.swc} J" ,className="card-text"),
                            dbc.Button("✎", color="secondary", className="me-1", n_clicks=0),
                        ]
                    )
                )

            ],
            className="mb-2",
        )

        offcanvas = html.Div(
            [
                config_view,
                dbc.Offcanvas(
                    html.P("This is configuration offcanvas"),
                    id="cyclometry_config_offcanvas",
                    title="Configuration",
                    is_open=False,
                )



            ]
        )
        return offcanvas
