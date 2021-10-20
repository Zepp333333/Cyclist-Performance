#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

from .presenter import Presenter, CalendarView
from .master_layout import MasterLayout


class AppPresenter(Presenter):
    """
    As part of MVP pattern interacts with Model (Logic) and provides formatted data to Dash View.
    """
    def __init__(self):
        """

        """

    def get_master_layout(self):
        return MasterLayout().layout

    def get_calendar(self) -> None:
        calendar = self.make_calendar()
        self.view.update_calendar_view(calendar)



    def make_calendar(self) -> CalendarView:
        pass
