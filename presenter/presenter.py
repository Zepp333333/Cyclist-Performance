#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

from abc import ABC, abstractmethod

import dash


class CalendarView:
    pass


class Presenter(ABC):
    """Base Presenter class"""
    def __init__(self):
        """"""

    @abstractmethod
    def get_master_layout(self) -> dash.Dash.layout:
        """"""
