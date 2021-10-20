#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import dash
from typing import Protocol, Optional
from abc import abstractmethod




class View(Protocol):
    """Protocol representing View of MVP Pattern"""
    presenter: object
    user_id: Optional[int] = None

    @abstractmethod
    def render_main(self) -> dash.Dash.layout:
        """Update main/home page view"""

    @abstractmethod
    def render_activity(self) -> dash.Dash.layout:
        """Update Activity View"""


class AppView:
    """Implement View Protocol"""

    def __init__(self, presenter_class):
        self.presenter = presenter_class(self)
        self.user_id: Optional[int] = None

    def render_main(self) -> dash.Dash.layout:
        """Update main/home page view"""

    def render_activity(self) -> dash.Dash.layout:
        """Update Activity View"""

    def render_power(self) -> dash.Dash.layout:
        """Update Power view"""
