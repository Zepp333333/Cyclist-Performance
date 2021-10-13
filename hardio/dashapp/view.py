#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

from abc import ABC, abstractmethod
import dash


class View(ABC):
    """Base class representing view of MVP Pattern"""

    @abstractmethod
    def page(self) -> dash.Dash.layout:
        pass
