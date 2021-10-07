#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

from abc import ABC

from hardio.dashapp.activity_main_new import ActivityView


class Presenter:
    pass


class ActivityPresenter:
    def __init__(self, view: ActivityView, user_id: int, activity_id: int):
        self.view = view

    def page(self):
        tabs = {
            'Activity': self.view.make_activity_tab(),
            'Power': self.view.make_power_tab()
        }
        self.view.page_tabs = self.view.make_page_tabs(tabs)
        return self.view.page()
