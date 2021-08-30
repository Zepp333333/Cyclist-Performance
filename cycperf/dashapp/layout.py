#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

# Styling the navbar
NAVBAR_STYLE = {
    "position": "fixed",
    "overflow": "hidden",
    "top": 0,
    "left": 0,
    "width": "100%",
    "background-color": "#5f788a"
}
# Styling the sidebar:
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "margin-top": "2rem"
}

# padding for the page content
CONTENT_STYLE = {
    "position": "relative",
    "margin-top": "2rem",
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

navbar = html.Div([
    html.Header([
        html.Nav([
            html.Div([
                html.A("Cyclist Performance", href="/Application/", className="navbar-brand mr-4")
            ], "Navbar_Container", className="container")
        ], "Navbar",
            className="navbar navbar-expand-md navbar-dark bg-steel fixed-top",
            style=NAVBAR_STYLE),
    ], "Header", className="site-header", ),
],

)

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.H3(id="username_placeholder", children=[], className="display-4"),
        html.Hr(),
        html.P("Some text here", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Calendar", href="/application/", active="exact"),
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
        navbar,
        sidebar,
        content,
        dcc.Store(id="current_activity")
    ]
)
