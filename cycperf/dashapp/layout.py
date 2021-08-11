#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


# Styling the sidebar:
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1 rem",
    "background-color": "#f8f9fa"
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.H3(id="username_placeholder", children=[], className="display-4"),
        html.Hr(),
        html.P("Some text here", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/application/", active="exact"),
                dbc.NavLink("Activity", href="/application/activity", active="exact"),
                dbc.NavLink("Something else", href="/application/else", active="exact"),
                dbc.NavLink("test", href="/application/test/12", active="exact"),
                dbc.NavLink("Test Strava Methods", href="/application/test_strava", active="exact")
            ],
            vertical=True,
            pills=True
        )
    ],
    style=SIDEBAR_STYLE
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

layout = html.Div(
    [
        dcc.Location(id="url"),
        sidebar,
        content,
        dcc.Store(id="current_activity")
    ]
)
