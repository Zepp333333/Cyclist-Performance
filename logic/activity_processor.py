#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
from __future__ import annotations

from typing import Optional

from logic import Activity, Derivative, RunningPace, MovingAverage


class ActivityProcessor:
    def __init__(self):
        self.streams_to_preprocess: list[str] = []
        self.derivatives_to_add: dict[str: Derivative()] = {}

    @classmethod
    def get_activity_processor(cls, details: dict) -> ActivityProcessor:
        processors = {
            "Ride": RideActivityProcessor,
            "VirtualRide": RideActivityProcessor,
            "Run": RunActivityProcessor,
        }

        if ('type' in details) and (details['type'] in processors):
            processor = processors[details['type']]
            return processor()
        else:
            return GenericActivityProcessor()

    def pre_process(self, activity: Activity) -> Activity:
        if activity.dataframe.empty:
            return activity
        processed_activity = self.add_derivatives(activity, self.derivatives_to_add)
        return processed_activity

    def add_derivatives(self, activity: Activity, derivatives_to_add: dict[str: Derivative()]) -> Activity:
        for derivative_name, derivative_object in derivatives_to_add.items():
            new_stream = derivative_object.produce(df=activity.dataframe, stream_name=derivative_name)
            activity.dataframe[derivative_name] = new_stream
        return activity


class RideActivityProcessor(ActivityProcessor):
    def __init__(self):
        super().__init__()
        self.derivatives_to_add = {'watts30': MovingAverage(stream='watts')}


class RunActivityProcessor(ActivityProcessor):
    def __init__(self):
        super().__init__()
        self.derivatives_to_add = {'pace': RunningPace(),
                                   'pace30': MovingAverage(stream='pace')}


class GenericActivityProcessor(ActivityProcessor):
    def pre_process(self, activity: Activity) -> Optional[Activity]:
        return activity

    def add_derivatives(self, activity: Activity, stream_name: str) -> Activity:
        return activity
