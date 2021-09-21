#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

import pandas as pd

DEFAULT_DURATIONS = [
        *range(1, 61),
        *range(65, 121, 5),
        *range(130, 310, 10),
        *range(330, 630, 30),
        *range(660, 3660, 60),
        *range(3900, 43500, 300)
    ]


def calculate_ride_cp(df: pd.DataFrame) -> pd.DataFrame:

    durations = []
    watts = []
    last_record = df['time'].max()

    for d in DEFAULT_DURATIONS:
        if d > last_record:
            break
        durations.append(d)
        watts.append(int(df['watts'].rolling(d).mean().max()))

    cp = pd.DataFrame().reindex(columns=['Duration', 'Watts'])
    cp['Duration'] = durations
    cp['Watts'] = watts
    return cp
