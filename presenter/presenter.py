#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import dash

import dash_html_components as html

from iobrocker import IO
from .master_layout import MasterLayout
from .modules import AppCalendar, CalendarFormatter, ActivityPresenter, Cyclometry
from .base_presenter import BasePresenter
from config import Config


class Presenter(BasePresenter):
    """
    As part of MVP pattern interacts with Model (Logic, IO) and provides formatted data to Dash View.
    """
    def __init__(self, view):
        super().__init__()
        self.view = view

    def get_master_layout(self):
        return MasterLayout().layout

    def get_calendar(self) -> dash.Dash.layout:
        context = self.view.context
        io = IO(self.view.current_user)
        formatter = CalendarFormatter()
        calendar = AppCalendar(io, formatter)
        return calendar.make_layout(context)

    def get_activity(self) -> dash.Dash.layout:
        context = self.view.context
        io = IO(self.view.current_user)
        if Config.CYCLOMETRY:
            return Cyclometry(io, context).make_layout()
        return ActivityPresenter(io, context).make_layout()
