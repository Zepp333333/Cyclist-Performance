import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import activity_main

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
        html.Hr(),
        html.P("Some text here", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Activity", href="/activity", active="exact"),
                dbc.NavLink("Something else", href="/else", active="exact"),
            ],
            vertical=True,
            pills=True
        )
    ],
    style=SIDEBAR_STYLE
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div(
    [
        dcc.Location(id="url"),
        sidebar,
        content
    ]
)

@app.callback(
    Output(component_id="page-content", component_property="children"),
    Input(component_id="url", component_property="pathname")
)
def render_page_content(pathname):
    if pathname == "/":
        return [
            html.H1("Home page", style={"textAlign": "center"}),
        ]
    elif pathname == "/activity":
        return [
            html.H1("Activity page", style={"textAlign": "center"}),
            activity_main.layout
        ]
    elif pathname == "/else":
        return [
            html.H1("Something Else page", style={"textAlign": "center"}),
        ]

    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not Found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognized...")
        ]
    )


# this is the layout and callback of a static 2-page app

# app.layout = html.Div([
#     dcc.Location(id='url', refresh=False),
#     html.Div([
#         dcc.Link('View Activity| ', href='/apps/activity'),
#         dcc.Link('Another View Activity', href='/apps/another_activity'),
#     ], className="row"),
#     html.Div(id='page-content', children=[])
# ])


# @app.callback(Output('page-content', 'children'),
#               [Input('url', 'pathname')])
# def display_page(pathname):
#     if pathname == '/apps/activity':
#         return activity_main.layout
#     if pathname == '/apps/another_activity':
#         return activity_main.layout
#     else:
#         return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=True)
