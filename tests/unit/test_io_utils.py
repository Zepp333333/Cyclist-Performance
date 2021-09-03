#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import pandas as pd
import pytest
from datetime import datetime, timezone
import json
from iobrocker import CustomEncoder, CustomDecoder
from logic import Interval, CyclingInterval
from iobrocker import dbutil


@pytest.fixture()
def data():
    dataframe = dbutil.read_dataframe_from_csv()
    interval1 = CyclingInterval(id=1,
                               activity_id=123456,
                               name="Interval 1",
                               start=15,
                               end=250, dataframe=dataframe)
    interval2 = CyclingInterval(id=3,
                                activity_id=123456,
                                name="Interval 2",
                                start=155,
                                end=2555, dataframe=dataframe)
    return {
        "name": "Name",
        "activity_id": 12345,
        "dt": datetime(2021, 8, 17, 11, 40, 49, tzinfo=timezone.utc),
        "intervals": [interval1, interval2]
    }

@pytest.fixture()
def string():
    return """{
    "name": "Name",
    "activity_id": 12345,
    "dt": {
        "_type": "datetime",
        "value": "2021-08-17 11:40:49+0000"
    },
    "intervals": [
        {
            "_type": "CyclingInterval",
            "value": {
                "id": 1,
                "activity_id": 123456,
                "name": "Interval 1",
                "start": 15,
                "end": 250,
                "avg_power": 164.14893617021278,
                "max_power": 558.0,
                "min_power": 0.0,
                "avg_hr": 161.6212765957447,
                "max_hr": 173.0,
                "min_hr": 137.0,
                "avg_cad": 79.02155172413794,
                "max_cad": 114.0,
                "min_cad": 0.0
            }
        },
        {
            "_type": "CyclingInterval",
            "value": {
                "id": 3,
                "activity_id": 123456,
                "name": "Interval 2",
                "start": 155,
                "end": 2555,
                "avg_power": 271.2375,
                "max_power": 583.0,
                "min_power": 0.0,
                "avg_hr": 184.31666666666666,
                "max_hr": 189.0,
                "min_hr": 165.0,
                "avg_cad": 83.87333333333333,
                "max_cad": 141.0,
                "min_cad": 0.0
            }
        }
    ]
}
"""


def test_custom_encoder(data):
    string = json.dumps(data, cls=CustomEncoder, indent=4)
    assert isinstance(string, str)
    assert '"_type": "datetime"' in string
    assert '"value": "2021-08-17 11:40:49+0000"' in string
    assert '"_type": "CyclingInterval"' in string


def test_custom_decoder(string):
    d = json.loads(string, cls=CustomDecoder)
    assert isinstance(d, dict)
    assert isinstance(d['intervals'], list)
    assert len(d['intervals']) == 2
    assert isinstance(d['intervals'][0], Interval)
    assert isinstance(d['intervals'][1], Interval)
    assert d['intervals'][0].max_power == 558.0
    assert d['intervals'][1].max_power == 583.0
