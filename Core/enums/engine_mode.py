__author__ = 'shankar'

from enum import Enum

class EngineMode(Enum):
    init = 0
    stopped = 1
    paused = 2
    executing = 3
    training = 4
