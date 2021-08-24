#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import json
from datetime import datetime, timezone
from typing import Any
import numpy as np

import pandas as pd

from middleware import Interval, CyclingInterval, ActivityFactory, CyclingActivityFactory

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S%z'


class CustomEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        # datetime
        if isinstance(obj, datetime):
            return {
                "_type": "datetime",
                "value": obj.strftime(DATETIME_FORMAT)
            }

        # Interval
        if isinstance(obj, Interval):
            obj_dict = obj.__dict__
            if 'sort_index' in obj_dict.keys():
                obj_dict.pop('sort_index')  # remove sort_index as value of is is set in post_init
            return {
                "_type": obj.__class__.__name__,
                "value": obj.__dict__
            }

        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                            np.int16, np.int32, np.int64, np.uint8,
                            np.uint16, np.uint32, np.uint64)):
            return int(obj)

        if isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            return float(obj)

        # for other types - call default
        return json.JSONEncoder.default(self, obj)


class CustomDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if "_type" in obj:
            if obj['_type'] == 'datetime':
                return datetime.strptime(obj['value'], DATETIME_FORMAT)
            if obj['_type'] == 'CyclingInterval':
                return CyclingInterval(dataframe=pd.DataFrame(), **obj['value'])
        return obj


def get_activity_factory(details: dict) -> ActivityFactory:
    factories = {
        "Ride": CyclingActivityFactory
    }

    if 'type' in details:
        factory = factories[details['type']]
        return factory()
    else:
        return CyclingActivityFactory()


def datetime_from_string(string: str) -> datetime:
    return datetime.strptime(string, DATETIME_FORMAT)
