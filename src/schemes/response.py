import datetime

from src.schemes.base import SBase


class SResponse(SBase):
    dataset: list[int]
    labels: list[datetime.datetime]
