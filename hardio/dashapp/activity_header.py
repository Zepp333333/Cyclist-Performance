#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

from dataclasses import dataclass, field
from logic import Activity
import dash_html_components as html
import dash_bootstrap_components as dbc


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
        if activity.type == 'Run':
            return html.Div(
                [

                ]
            )

        line1 = dbc.ListGroup(
            [
                dbc.ListGroupItem(
                    [
                        dbc.ListGroupItemHeading(activity.name, style={'font-size': '1rem'}),
                        dbc.ListGroupItemText(activity.date),
                        dbc.ListGroupItemText(""),
                    ]
                ),
                dbc.ListGroupItem(
                    [
                        dbc.ListGroupItemHeading("Power", style={'font-size': '1rem'}),
                        dbc.ListGroupItemText(f"Avg power: {activity.intervals[0].avg_power} text"),
                        dbc.ListGroupItemText(f"Max power: {activity.intervals[0].max_power}"),

                    ]
                ),
                dbc.ListGroupItem(
                    [
                        dbc.ListGroupItemHeading("HR", style={'font-size': '1rem'}),
                        dbc.ListGroupItemText(f"Avg HR: {activity.intervals[0].avg_hr}"),
                        dbc.ListGroupItemText(f"Max HR: {activity.intervals[0].max_hr}"),

                    ]
                ),
            ],
            horizontal=True,
            className="mb-1",
            style={'font-size': '0.8rem'},
        )

        line2 = dbc.ListGroup(
            [

            ]
        )

        list_group = html.Div(
            [
                line1,
                line2,
            ]
        )
        return list_group
