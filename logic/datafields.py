#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

from abc import ABC, abstractmethod
from dataclasses import dataclass

import pandas as pd
from datetime import datetime


@dataclass
class DataFields:
    date: datetime = None
    name: str = None
    sport: str = None
    weight: float = None
    RPE: int = None
    keyword: str = None
    notes: str = None
    device: str = None
    recording_interval: int = None
    duration: float = None
    time_moving: float = None
    distance: float = None
    work: float = None
    elevation_gain: float = None
    average_speed: float = None
    average_power: float = None
    average_hr: float = None
    average_cad: float = None
    TSS: float = None
    CP: float = None



