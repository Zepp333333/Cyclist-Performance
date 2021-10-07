#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

from presenter import ActivityPresenter
from .activity_main_new import ActivityView


class ActivityPage:
    def __init__(self, user_id: int, activity_id: int):
        view = ActivityView()
        self.presenter = ActivityPresenter(view, user_id, activity_id)

    def render(self):
        return self.presenter.page()
