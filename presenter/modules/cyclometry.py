#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
from __future__ import annotations

import gzip
import json
from datetime import datetime, timedelta

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

from .utils.scatter_drawer2 import ScatterDrawer


class CActivity:
    """
    Represents Cyclometry Activity
    """

    def __init__(self, activity_json):
        self.activity_json = activity_json
        self.tags = self.activity_json['RIDE']['TAGS']
        self.samples = self.activity_json['RIDE']['SAMPLES']
        self.identifier = self.activity_json['RIDE']['IDENTIFIER']
        self.start_time = datetime.strptime(self.activity_json['RIDE']['STARTTIME'], '%Y/%m/%d %H:%M:%S %Z')
        self.recording_interval = self.activity_json['RIDE']['RECINTSECS']
        self.df = self.samples_to_df(self.samples)
        self.duration = timedelta(seconds=int(self.df['SECS'].max()))
        self.avg_power = int(self.df['WATTS'].mean())
        self.avg_HR = int(self.df['HR'].mean())
        self.max_power = int(self.df['WATTS'].max())
        self.max_HR = int(self.df['HR'].max())



    @classmethod
    def from_file(cls, path: str) -> CActivity:
        with gzip.open(path, 'r') as f:
            return cls(json.load(f))

    def samples_to_df(self, samples):
        normalized = self.normalize_samples(samples)
        return pd.DataFrame(normalized)

    def normalize_samples(self, samples):
        for s, i in zip(samples, range(len(samples))):
            s['SECS'] = i
        return samples


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
        return CActivity.from_file('temp/2021-04-21_14-26-50.json')

    def make_header(self, c_activity: CActivity):
        header = html.Div(
            [
                dbc.Row(dbc.Col(html.Div(f"Activity: {c_activity.identifier}"))),
                dbc.Row(
                    [
                        dbc.Col(html.Div(f"Date: {c_activity.start_time.strftime('%b %m, %Y')}"), width=2),
                        dbc.Col(html.Div(f"AVG Power: {c_activity.avg_power}"), width=2),
                        dbc.Col(html.Div(f"AVG HR: {c_activity.avg_HR}"), width=2),
                        dbc.Col(html.Div(f"AWC below Zero:"), width=2),
                        dbc.Col(html.Div(f"CP and AWC Stress:"), width=2),
                        dbc.Col(html.Div(f"Total Work:"), width=2),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(html.Div(f"Duration: {c_activity.duration}"), width=2),
                        dbc.Col(html.Div(f"MAX Power: {c_activity.max_power}"), width=2),
                        dbc.Col(html.Div(f"MAX HR: {c_activity.max_HR}"), width=2),
                        dbc.Col(html.Div(f"SWC below Zero"), width=2),
                        dbc.Col(html.Div(f"GP and SC Stress"), width=2),
                        dbc.Col(html.Div(f"CH and Fat"), width=2),
                    ],
                ),

            ]
        )

        return header

    def make_fig(self, c_activity):
        drawer = ScatterDrawer(df=c_activity.df, index_col='SECS',
                               series_to_plot=[s for s in c_activity.df.columns if s != 'SECS'])
        fig = drawer.get_fig()
        return fig
