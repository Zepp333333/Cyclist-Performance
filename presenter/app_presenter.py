#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import dash

from iobrocker import IO
from .master_layout import MasterLayout
from .modules import AppCalendar, CalendarFormatter
from .presenter import Presenter


class AppPresenter(Presenter):
    """
    As part of MVP pattern interacts with Model (Logic, IO) and provides formatted data to Dash View.
    """
    def __init__(self, view):
        super().__init__()
        self.view = view

    def get_master_layout(self):
        return MasterLayout().layout

    def get_calendar(self) -> None:
        calendar = self.make_calendar()
        return calendar

    def make_calendar(self) -> dash.Dash.layout:
        context = self.view.context
        io = IO(self.view.current_user)
        formatter = CalendarFormatter()
        calendar = AppCalendar(io, formatter)
        return calendar.make_layout(context)
