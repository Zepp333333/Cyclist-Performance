#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import pytest
from logic import IntervalList, CyclingInterval, RunningInterval
from logic.interval_factory import CyclingIntervalFactory, RunningIntervalFactory


@pytest.fixture
def mock_list_of_intervals(mock_activity):
    lst = []
    factory = CyclingIntervalFactory()
    for i in range(5):
        interval = factory.get_interval().create(id=i,
                                                 activity_id=mock_activity.id,
                                                 name=f'interval {i}',
                                                 start=i * 100+30,
                                                 end=i * 110+50,
                                                 dataframe=mock_activity.dataframe)
        lst.append(interval)
    factory = RunningIntervalFactory()
    lst.append(factory.get_interval())
    return lst


class TestIntervalList:

    def test_init(self, mock_list_of_intervals):
        ilist1 = IntervalList()
        ilist2 = IntervalList(mock_list_of_intervals)
        assert isinstance(ilist1, IntervalList)
        assert isinstance(ilist2, IntervalList)

    def test_to_json(self, mock_list_of_intervals):
        ilist2 = IntervalList(mock_list_of_intervals)
        string = ilist2.to_json()
        assert isinstance(string, str)
        assert '_type' in string
        assert 'RunningInterval' in string

    def test_from_json(self, mock_list_of_intervals):
        ilist = IntervalList(mock_list_of_intervals)
        string = ilist.to_json()
        restored = IntervalList.from_json(string)
        assert isinstance(restored, IntervalList)
        assert len(restored) == 6
        assert isinstance(restored[0], CyclingInterval)
        assert isinstance(restored[5], RunningInterval)
        assert restored[1].name == 'interval 1'
        assert restored[2].start == 230
