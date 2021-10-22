#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class AppModule:
    display_name: str
    route: str

@dataclass
class Button:
    name: str
    id: str

@dataclass
class Input:
    id: str
    type: str = "number"
    placeholder: str = ""

    def expand(self):
        return f"id={self.id}, type={self.type}, placeholder={self.placeholder}"

@dataclass
class Tab:
    label: str
    tab_id: str


class Tabs:
    activity_tab = Tab("Activity", "activity_tab")
    power_tab = Tab("Power", "power_tab")

class Inputs:
    interval_duration = Input("interval_duration", "number", "Set interval length")
    how_many_to_find = Input("how_many_to_find", "number", "How many to find")
    interval_power = Input("interval_power", "number", "Interval Power, wt")
    interval_tolerance = Input("interval_tolerance", "number", "Tolerance %")

class Buttons:
    refresh_activities = Button("Refresh", "btn_refresh_activities")
    create_interval = Button("Create Interval", "btn_create_interval")
    find_intervals = Button("Find Intervals", "btn_find_intervals")
    delete_intervals = Button("Delete Intervals", "btn_delete_intervals")


class AppDashIDs:
    user_name_placeholder = "username_placeholder"
    page_content = "page_content"
    url = "url"
    activity_store = "current_activity_store"
    user_config_store = "user_config_store"
    navbar_container = "navbar_container"
    navbar = "navbar"
    site_header = "site_header"
    calendar = "calendar"
    spinner = "refresh_spinner"
    calendar_refresh_alert = "calendar_refresh_alert"
    calendar_table = "calendar_table"
    calendar_month_selector = "calendar_month_selector"
    activity_main_chart = "activity_main_chart"
    activity_cp_chart = "activity_cp_chart"
    activity_tabs = "activity_tabs"


class AppModules:
    calendar = AppModule("Calendar", "/application/")
    activity = AppModule("Activity", "/application/activity/")
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
