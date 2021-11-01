#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

from abc import ABC, abstractmethod

import dash


class BasePresenter(ABC):
    """Base Presenter class"""
    def __init__(self):
        """"""

    @abstractmethod
    def get_master_layout(self) -> dash.Dash.layout:
        """Produce Master Dash-app Layout"""

    @abstractmethod
    def get_calendar(self) -> dash.Dash.layout:
        """Produce Calendar view"""

    @abstractmethod
    def get_activity(self) -> dash.Dash.layout:
        """Produce Activity view"""

    @abstractmethod
    def save_config_and_update_page(self):
        """save user_config and refresh an activity page"""
