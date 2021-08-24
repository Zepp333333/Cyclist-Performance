#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
"""
IO library for Cyclist Performance application
Provides high level interface to data management and retrieval from Strava.com as well as from/to database
"""

# todo rename iobrocker to io_lib
# todo low level strava_auth interface still used in user routes -> uplift it to IO
from .iowrapper import IO
from .utils import CustomEncoder, CustomDecoder

