#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
from __future__ import annotations

from abc import ABC
from typing import Optional

from logic import Activity, MovingAverage


class ActivityProcessor(ABC):
    def __init__(self):
        self.streams_to_preprocess: list[str] = []

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
        processed_activity = self.add_derivatives(activity, self.streams_to_preprocess)
        return processed_activity

    def add_derivatives(self, activity: Activity, streams: list[str]) -> Activity:
        for stream in streams:
            if stream in activity.dataframe:
                produced_stream = MovingAverage().produce(activity.dataframe[stream])
                activity.dataframe[f'{stream}30'] = produced_stream
        return activity


class RideActivityProcessor(ActivityProcessor):
    def __init__(self):
        super().__init__()
        self.streams_to_preprocess = ['watts']


class RunActivityProcessor(ActivityProcessor):
    def __init__(self):
        super().__init__()
        self.streams_to_preprocess = ['velocity_smooth']

    def pre_process(self, activity: Activity) -> Activity:
        return activity


class GenericActivityProcessor(ActivityProcessor):
    def pre_process(self, activity: Activity) -> Optional[Activity]:
        return activity

    def add_derivatives(self, activity: Activity, stream_name: str) -> Activity:
        return activity
