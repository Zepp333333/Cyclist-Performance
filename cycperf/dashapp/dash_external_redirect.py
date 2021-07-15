#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import dash_core_components as dcc
import dash_html_components as html


def redirect(url):
    return html.Div(dcc.Location(id="redirect", href=url, refresh=True))
