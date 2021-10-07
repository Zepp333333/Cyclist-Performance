#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

from abc import ABC, abstractmethod


class View(ABC):
    """Base class representing view of MVP Pattern"""

    @abstractmethod
    @property
    def page(self):
        pass
