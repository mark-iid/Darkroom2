from enum import Enum


# battery status
class Status(Enum):
    OFF = 'off'
    ON = 'on'


# battery config object
class GridItem:
    def __init__(self, name, label, status, key):
        self.name = name
        self.label = label
        self.status = status
        self.key = key