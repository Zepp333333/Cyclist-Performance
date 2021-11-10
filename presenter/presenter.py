#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import dash

from datetime import datetime, timezone

from config import Config
from iobrocker import IO
from .base_presenter import BasePresenter
from .master_layout import MasterLayout
from .modules import AppCalendar, CalendarFormatter, ActivityPresenter, Cyclometry


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

    def save_config_and_update_page(self):
        context = self.view.context
        io = IO(self.view.current_user)
        config = io.read_user_config()
        config.activity_config.charts_to_plot = context['switches']
        io.save_user_config(config)
        return ActivityPresenter(io, context).make_layout(), config

    def update_cyclometry_view(self):
        context = self.view.context
        io = IO(self.view.current_user)
        c = Cyclometry(io, context)
        c.api_request_update()

    def activity_create_intervals_and_refresh_view(self):
        context = self.view.context

        intervals_range = self._relayout_data_to_range(context['intervals_range'])

        activity_id = int(context['activity'])
        io = IO(self.view.current_user)
        config = io.read_user_config()
        if intervals_range:
            activity = io.get_hardio_activity_by_id(activity_id)
            activity.add_interval(*intervals_range)
            io.save_activity(activity)
            return ActivityPresenter(io, context).make_figure(activity, config)
        else:
            return dash.no_update

    def activity_delete_intervals_and_refresh_view(self):
        context = self.view.context
        activity_id = int(context['activity'])
        io = IO(self.view.current_user)
        config = io.read_user_config()
        activity = io.get_hardio_activity_by_id(activity_id)
        activity.delete_intervals()
        io.save_activity(activity)
        return ActivityPresenter(io, context).make_figure(activity, config)

    def activity_find_intervals_and_refresh_view(self):
        context = self.view.context
        activity_id = int(context['activity'])
        io = IO(self.view.current_user)
        config = io.read_user_config()
        activity = io.get_hardio_activity_by_id(int(activity_id))
        interval_finder_params = context['interval_finder_prams']
        found_intervals = activity.find_intervals(**interval_finder_params)
        activity.add_intervals(found_intervals)
        io.save_activity(activity)
        return ActivityPresenter(io, context).make_figure(activity, config)

    def _relayout_data_to_range(self, relayout_data: dict) -> tuple[int, int]:
        """Helper fuction converting relaout_daya dict to tuple"""

        def relayout_data_to_int(s: str) -> int:
            d = datetime.strptime(s, '%Y-%m-%d %H:%M:%S.%f')
            d = d.replace(tzinfo=timezone.utc)
            return int(d.timestamp())

        try:
            if len(relayout_data) == 1:
                return relayout_data_to_int(relayout_data['xaxis.range'][0]), relayout_data_to_int(relayout_data['xaxis.range'][1])
            else:
                result = [relayout_data_to_int(v) for v in relayout_data.values()]
                return result[0], result[1]
        except KeyError:
            return tuple()
