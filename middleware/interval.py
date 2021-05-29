#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved


class Interval:
    def __init__(self,
                 activity: 'Activity',
                 title: str,
                 start: int,
                 end: int,
                 ):

        self.activity = activity
        self.title = title
        self.start = start
        self.end = end
        self.df = None

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

        self.populate_metrics()

    def populate_metrics(self) -> None:
        self.df = self.activity.df.iloc[self.start:self.end]
        if 'watts' in self.df:
            self.populate_watts()
        if 'heartrate' in self.df:
            self.populate_hr()
        if 'cadence' in self.df:
            self.populate_cad()
        del self.df

    def populate_watts(self) -> None:
        self.avg_power = self.df.watts.mean()
        self.max_power = self.df.watts.max()
        self.min_power = self.df.watts.min()

    def populate_hr(self) -> None:
        self.avg_hr = self.df.heartrate.mean()
        self.max_hr = self.df.heartrate.max()
        self.min_hr = self.df.heartrate.min()

    def populate_cad(self) -> None:
        self.avg_cad = self.df.cadence.mean()
        self.max_cad = self.df.cadence.max()
        self.min_cad = self.df.cadence.min()

    def __eq__(self, other) -> bool:
        return self.range == other.range
