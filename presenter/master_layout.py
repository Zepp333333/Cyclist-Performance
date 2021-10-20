#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from presenter import AppConfig as Config
from presenter import AppDashIDs as IDs


class MasterLayout:
    def __init__(self):
        self.layout = self.make_layout()

    def make_layout(self) -> dash.Dash.layout:
        navbar = self.make_navbar()
        sidebar = self.make_sidebar()
        content = self.make_content()
        return html.Div(
            [
                dcc.Location(id=IDs.url),
                navbar,
                sidebar,
                content,
                dcc.Store(id=IDs.activity_store),
                dcc.Store(id=IDs.user_config_store, storage_type='session'),
            ]
        )

    def make_navbar(self):
        return html.Div(
            [
                html.Header(
                    [
                        html.Nav(
                            [
                                html.Div(
                                    [
                                        html.A(Config.APP_NAME, href=Config.SITE_ROOT, className="navbar-brand mr-4")
                                    ],
                                    "Navbar_Container", className="container"
                                )
                            ],
                            "Navbar",
                            className="navbar navbar-expand-md navbar-dark bg-steel fixed-top",
                            style=Config.NAVBAR_STYLE
                        ),
                    ],
                    "Header", className="site-header",
                ),
            ],
        )

    def make_sidebar(self):
        sidebar_links = [dbc.NavLink(o.display_name, href=o.route, active="exact") for o in Config.SIDEBAR_OPTIONS]
        return html.Div(
            [
                html.H3(id=IDs.user_name_placeholder, children=[], className="display-5"),
                html.Hr(),
                dbc.Nav(
                    sidebar_links,
                    vertical=True,
                    pills=True
                )
            ],
            style=Config.SIDEBAR_STYLE
        )

    def make_content(self):
        return html.Div(id=IDs.page_content, children=[], style=Config.CONTENT_STYLE)
