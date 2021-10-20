#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class AppModule:
    display_name: str
    route: str


class AppDashIDs:
    user_name_placeholder = "username_placeholder"
    page_content = "page_content"
    url = "url"
    activity_store = "current_activity_store"
    user_config_store = "user_config_store"
    navbar_container = "navbar_Container"
    navbar = "navbar"
    site_header = 'site_header'

class AppModules:
    calendar = AppModule("Calendar", "/application/")
    power = AppModule("Power", "/application/power/")
    fitness = AppModule("Fitness", "/application/fitness/")
    config = AppModule("Config", "/config/")


class AppConfig:
    APP_NAME = "HARDIO"
    SITE_ROOT = "/"
    SIDEBAR_OPTIONS = [
        AppModules.calendar,
        AppModules.power,
        AppModules.fitness,
        AppModules.config
    ]

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
        "width": "10rem",
        "padding": "2rem 1rem",
        "background-color": "#f8f9fa",
        "margin-top": "2rem"
    }

    # padding for the page content
    CONTENT_STYLE = {
        "position": "relative",
        "margin-top": "2rem",
        "margin-left": "11rem",
        "margin-right": "1rem",
        "padding": "2rem 1rem",
    }
