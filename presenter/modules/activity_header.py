#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

from dataclasses import dataclass, field
from logic import Activity, ActivityMetrics
import dash_bootstrap_components as dbc
from dash import html


@dataclass
class HeaderField:
    value: str = ''
    style: dict[str: str] = field(default_factory=dict[str: str])


@dataclass
class HeaderBox:
    heading: str = ''
    fields: list[HeaderField] = field(default_factory=list[HeaderField])


@dataclass
class HeaderRow:
    row_num: int = 0
    boxes: list[HeaderBox] = field(default_factory=list[HeaderBox])


@dataclass()
class ActivityHeader:
    boxes = {
        'base_info': [],
        'load': [],
        'hr': [],
        'power': [],
        'power2': [],
        'power3': [],
    }

    @staticmethod
    def make_activity_info_header(activity: Activity):
        if activity.type == ('Run' or 'Walk'):
            return html.Div(
                [

                ]
            )
        metrics = ActivityMetrics(activity=activity, config={'ftp': 290})
        line1 = dbc.ListGroup(
            [
                dbc.ListGroupItem(
                    [
                        dbc.ListGroupItem(activity.name, style={'font-size': '0.7rem'}),
                        dbc.ListGroupItem(activity.date),
                        dbc.ListGroupItem(""),
                    ],
                    style={'font-size': '0.6rem', 'line-height': '0.1em'}
                ),
                dbc.ListGroupItem(
                    [
                        dbc.ListGroupItem("Power", style={'font-size': '0.7rem'}),
                        dbc.ListGroupItem(f"{metrics.average_power}"),
                        dbc.ListGroupItem(f"{metrics.normalized}"),
                        dbc.ListGroupItem(f"{metrics.work}"),
                    ],
                    style={'font-size': '0.6rem', 'line-height': '0.1em'}
                ),
                dbc.ListGroupItem(
                    [
                        dbc.ListGroupItem("HR", style={'font-size': '0.7rem'}),
                        dbc.ListGroupItem(f"{metrics.average_hr}"),
                        dbc.ListGroupItem(f"{metrics.max_hr}"),
                    ],
                    style={'font-size': '0.6rem', 'line-height': '0.1em'}
                ),
            ],
            flush=True,
            horizontal=True,
            className="mb-1",
            style={'font-size': '0.8rem'},
        )

        # line2 = dbc.ListGroup(
        #     [
        #
        #     ],
        #     flush=True,
        # )

        list_group = html.Div(
            [
                line1,
                # line2,
            ],
        )
        return list_group
