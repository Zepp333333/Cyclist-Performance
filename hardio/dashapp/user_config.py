#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
from __future__ import annotations
from dataclasses import dataclass, field
import json
from typing import Any

@dataclass
class ActivityConfig:
    charts_to_plot: list = field(default_factory=list[str])

    def __post_init__(self):
        if not self.charts_to_plot:
            self.charts_to_plot = ['heartrate', 'cadence']


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
