#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import pandas as pd

from middleware import Activity, CyclingActivity
from middleware.interval import Interval
from middleware.interval_factory import CyclingIntervalFactory


class TestActivity:

    def test_activity_init(self, mock_activity):
        assert isinstance(mock_activity, Activity)
        assert isinstance(mock_activity, CyclingActivity)

    def test_make_whole_activity_interval(self, mock_activity):
        interval = mock_activity.make_whole_activity_interval()
        assert interval.id == 0
        assert interval.activity_id == mock_activity.id
        assert interval.start == 0
        assert interval.end == mock_activity.dataframe.last_valid_index()
        assert pd.DataFrame(interval.dataframe).empty

    def test_new_interval(self, mock_activity):
        mock_activity.new_interval(start=130, end=1330)
        mock_activity.new_interval(start=230, end=2330, name='New Name')
        assert len(mock_activity.intervals) == 3
        assert mock_activity.intervals[1].activity_id == mock_activity.id
        assert mock_activity.intervals[1].start == 130
        assert mock_activity.intervals[1].end == 1330
        assert mock_activity.intervals[1].name == 'Interval 1'
        assert mock_activity.intervals[2].activity_id == mock_activity.id
        assert mock_activity.intervals[2].start == 230
        assert mock_activity.intervals[2].end == 2330
        assert mock_activity.intervals[2].name == 'New Name'

    def test_add_intervals(self, mock_activity):
        factory = CyclingIntervalFactory().get_interval()
        factory2 = CyclingIntervalFactory().get_interval()
        interval1 = factory.create(id=15,
                                   activity_id=mock_activity.id,
                                   name='test interval name',
                                   start=15,
                                   end=150,
                                   dataframe=pd.DataFrame()
                                   )
        interval2 = factory2.create(id=16,
                                    activity_id=mock_activity.id,
                                    name='test interval name 2',
                                    start=150,
                                    end=250,
                                    dataframe=pd.DataFrame()
                                    )
        mock_activity.add_intervals([interval1, interval2])
        assert len(mock_activity.intervals) == 3
        assert mock_activity.intervals[1].activity_id == mock_activity.id
        assert mock_activity.intervals[1].id == 15
        assert mock_activity.intervals[1].start == 15
        assert mock_activity.intervals[1].end == 150
        assert mock_activity.intervals[1].name == 'test interval name'
        assert mock_activity.intervals[2].activity_id == mock_activity.id
        assert mock_activity.intervals[2].start == 150
        assert mock_activity.intervals[2].end == 250
        assert mock_activity.intervals[2].name == 'test interval name 2'

    def test_make_interval(self, mock_activity):
        interval = mock_activity.make_interval(start=600, end=700, name='new name')
        assert isinstance(interval, Interval)
        assert interval.activity_id == mock_activity.id
        assert interval.id == 1
        assert interval.start == 600
        assert interval.end == 700
        assert interval.name == 'new name'

    def test_generate_interval_name(self, mock_activity):
        name1 = mock_activity._generate_interval_name()
        mock_activity.new_interval(15, 20)
        name2 = mock_activity._generate_interval_name()

        assert name1 == 'Interval 1'
        assert name2 == 'Interval 2'

    def test_remove_intervals(self, mock_activity):
        mock_activity.new_interval(15, 20)
        mock_activity.new_interval(50, 60)
        assert len(mock_activity.intervals) == 3
        interval_to_remove1 = mock_activity.intervals[1]
        interval_to_remove2 = mock_activity.intervals[2]
        mock_activity.remove_intervals([interval_to_remove1, interval_to_remove2])
        assert len(mock_activity.intervals) == 1
        assert mock_activity.intervals[0].name == 'Whole Activity'

    def test_check_if_interval_exit(self, mock_activity):
        interval = mock_activity.intervals[0]
        interval2 = mock_activity.make_interval(400, 500)
        assert mock_activity.check_if_interval_exit(interval)
        assert not mock_activity.check_if_interval_exit(interval2)
