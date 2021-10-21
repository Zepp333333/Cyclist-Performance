#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
from typing import Optional
from abc import ABC
from flask_login import current_user
from dash_extensions.enrich import DashProxy
from presenter import Presenter


class View(ABC):
    """Base class representing View in MVP pattern"""
    presenter: Presenter
    _context: Optional[str] = None

    @property
    def current_user(self):
        return current_user.id if current_user else None

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, ctx):
        self._context = ctx


class CustomDashView(DashProxy, View):
    def __init__(self, presenter: Presenter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # noinspection PyCallingNonCallable
        self.presenter = presenter(self)
        self._context: Optional[str] = None
