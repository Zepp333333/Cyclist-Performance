#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PresentationActivity:
    id: int
    date: datetime
    name: str
    type: str
