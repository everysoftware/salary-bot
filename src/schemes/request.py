import datetime

from .base import SBase


class SRequest(SBase):
    dt_from: datetime.datetime
    dt_upto: datetime.datetime
    group_type: str
