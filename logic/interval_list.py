#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

# todo delete whole file as all functions implemented within Activity class

from __future__ import annotations

import json
from collections import UserList
from typing import Any

from logic import Interval, CyclingInterval, RunningInterval


class IntervalList(UserList):
    """
    Class implements list behaviour to hold list of Intervals. In addition provides to/from_json
    methods to enable storage
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def to_json(self) -> str:
        def _interval_encoder(obj: Any) -> Any:
            if isinstance(obj, Interval):
                return {
                    "_type": obj.__class__.__name__,
                    "value": obj.__dict__
                }
            if isinstance(obj, IntervalList):
                return {
                    "_type": obj.__class__.__name__,
                    "value": obj.__dict__
                }
            return json.JSONEncoder().default(obj)
        return json.dumps(self, default=_interval_encoder, indent=4)

    @classmethod
    def from_json(cls, string) -> IntervalList:
        def _object_hook(obj):
            if '_type' in obj:
                if obj['_type'] == 'IntervalList':
                    return IntervalList(obj['value'])
                if obj['_type'] == 'CyclingInterval':
                    return CyclingInterval(**obj['value'])
                if obj['_type'] == 'RunningInterval':
                    return RunningInterval(**obj['value'])
            if 'data' in obj:
                return obj['data']
            return obj
        return json.loads(string, object_hook=_object_hook)


from logic.interval_factory import CyclingIntervalFactory, RunningIntervalFactory
l = []
for i in range(5):
    l.append(CyclingIntervalFactory().get_interval())
ilist = IntervalList(l)
ilist.append(RunningIntervalFactory().get_interval())

s = ilist.to_json()

