#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import pandas as pd
import pytest

from logic import Activity
from logic.activity_processor import (
    ActivityProcessor,
    RideActivityProcessor,
    RunActivityProcessor,
    GenericActivityProcessor
)


class TestActivityProcessor:
    def test_init(self):
        processor = ActivityProcessor()
        assert isinstance(processor, ActivityProcessor)
        assert processor.streams_to_preprocess == []

    def test_get_activity_processor(self, mock_activity):
        ride_processor = ActivityProcessor.get_activity_processor(mock_activity.details)
        v_ride_processor = ActivityProcessor.get_activity_processor({"type": "VirtualRide"})
        run_processor = ActivityProcessor.get_activity_processor({"type": "Run"})
        swim_processor = ActivityProcessor.get_activity_processor({"type": "Swim"})
        other_processor = ActivityProcessor.get_activity_processor({"type": "other"})
        no_type_processor = ActivityProcessor.get_activity_processor({})

        assert isinstance(ride_processor, RideActivityProcessor)
        assert isinstance(v_ride_processor, RideActivityProcessor)
        assert isinstance(run_processor, RunActivityProcessor)
        assert isinstance(swim_processor, GenericActivityProcessor)
        assert isinstance(other_processor, GenericActivityProcessor)
        assert isinstance(no_type_processor, GenericActivityProcessor)

    def test_pre_process(self, mock_activity):
        processor = ActivityProcessor.get_activity_processor(mock_activity.details)
        processed_activity = processor.pre_process(activity=mock_activity)
        assert isinstance(processed_activity, Activity)
        assert 'watts30' in processed_activity.dataframe.columns

        # Run activity
        mock_activity.details = {"type": "Run"}
        processor = ActivityProcessor.get_activity_processor(mock_activity.details)
        processed_activity = processor.pre_process(activity=mock_activity)
        assert processed_activity == mock_activity

        # Other activity
        mock_activity.details = {}
        processor = ActivityProcessor.get_activity_processor(mock_activity.details)
        processed_activity = processor.pre_process(activity=mock_activity)
        assert processed_activity == mock_activity

    def test_pre_process_with_empty_dataframe(self, mock_activity):
        mock_activity.dataframe = pd.DataFrame()
        processor = ActivityProcessor.get_activity_processor(mock_activity.details)
        processed_activity = processor.pre_process(activity=mock_activity)
        assert processed_activity == mock_activity
