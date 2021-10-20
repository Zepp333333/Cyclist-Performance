#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

from .presenter import Presenter, CalendarView
from hardio.dashapp import View


class AppPresenter(Presenter):
    """
    As part of MVP pattern interacts with Model (Logic) and provides formatted data to Dash View.
    """
    def __init__(self, view: View):
        self.view = view


    def get_main_view(self, user_id: int):
        main_view = MainViewPresenter(user_id)
        self.view.update_main_view(main_view)

    def get_calendar(self) -> None:
        calendar = self.make_calendar()
        self.view.update_calendar_view(calendar)



    def make_calendar(self) -> CalendarView:
        pass


class MainViewPresenter:
    """

    """


class CalendarPresenter:
    """

    """


class ActivityPresenter:
    """

    """
