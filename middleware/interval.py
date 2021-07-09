#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
import pandas
import json


class Interval:
    def __init__(self,
                 activity_id: int,
                 df: pandas.DataFrame,
                 name: str,
                 start: int,
                 end: int,
                 ):

        self.activity_id = activity_id
        self.name = name
        self.start = start
        self.end = end

        self.range = self.start, self.end

        self.avg_power: int = 0
        self.max_power: int = 0
        self.min_power: int = 0

        self.avg_hr: int = 0
        self.max_hr: int = 0
        self.min_hr: int = 0

        self.avg_cad: int = 0
        self.max_cad: int = 0
        self.min_cad: int = 0

        self.populate_metrics(df.iloc[self.start:self.end])

    def populate_metrics(self, df) -> None:
        if 'watts' in df:
            self.populate_watts(df)
        if 'heartrate' in df:
            self.populate_hr(df)
        if 'cadence' in df:
            self.populate_cad(df)

    def populate_watts(self, df) -> None:
        self.avg_power = df.watts.mean()
        self.max_power = df.watts.max()
        self.min_power = df.watts.min()

    def populate_hr(self, df) -> None:
        self.avg_hr = df.heartrate.mean()
        self.max_hr = df.heartrate.max()
        self.min_hr = df.heartrate.min()

    def populate_cad(self, df) -> None:
        self.avg_cad = df.cadence.mean()
        self.max_cad = df.cadence.max()
        self.min_cad = df.cadence.min()

    def __eq__(self, other) -> bool:
        return self.range == other.range

    def to_json(self) -> json:
        return json.dumps(vars(self), indent=4)

