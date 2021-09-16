#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, ClassVar


@dataclass
class ActivityConfig:
    CHARTS_PRIORITY: ClassVar[dict[str:int]] = {
        'watts': 0,
        'pace': 0,
        'watts_30sec': 2,
        'heartrate': 4,
        'cadence': 6,
        'altitude': 8,
        'velocity_smooth': 10,
        'distance': 12,
        'grade_smooth': 14,
        'temp': 16,
        'moving': 30,
        'latlng': 40,
        'time': 50
    }
    _charts_to_plot: list[str] = field(default_factory=list[str])

    def __post_init__(self):
        if not self._charts_to_plot:
            self.charts_to_plot = ['heartrate', 'cadence']

    @property
    def charts_to_plot(self) -> dict[int:str]:
        return self._charts_to_plot

    @charts_to_plot.setter
    def charts_to_plot(self, charts_list: list[str]) -> None:
        charts_dict = {self.CHARTS_PRIORITY[chart]: chart for chart in charts_list}
        sorted_charts_dict = dict(sorted(charts_dict.items()))
        self._charts_to_plot = [v for v in sorted_charts_dict.values()]

    def __repr__(self):
        return f"{self.__class__.__name__}={self.__dict__} "

@dataclass
class ZonesConfig:
    ftp: int = 300
    z1: int = ftp * 0.55
    z2: int = ftp * 0.75
    z3: int = ftp * 0.90
    z4: int = ftp * 1.05
    z5: int = ftp * 1.2
    z6: int = ftp * 1.5
    Z7: int = ftp * 5


@dataclass
class UserConfig:
    activity_config: ActivityConfig = ActivityConfig()
    zones: ZonesConfig = ZonesConfig()

    def to_json(self) -> str:
        def _interval_encoder(obj: Any) -> Any:
            if isinstance(obj, (UserConfig, ActivityConfig, ZonesConfig)):
                return {
                    "_type": obj.__class__.__name__,
                    "value": obj.__dict__
                }
            return json.JSONEncoder().default(obj)

        return json.dumps(self, default=_interval_encoder, indent=4)

    @classmethod
    def from_json(cls, string) -> UserConfig:
        if not string:
            return UserConfig()

        def _object_hook(obj):
            if '_type' in obj:
                if obj['_type'] == 'UserConfig':
                    return UserConfig(**obj['value'])
                if obj['_type'] == 'ActivityConfig':
                    return ActivityConfig(**obj['value'])
                if obj['_type'] == 'ZonesConfig':
                    return ZonesConfig(**obj['value'])
            if 'data' in obj:
                return obj['data']
            return obj

        return json.loads(string, object_hook=_object_hook)
