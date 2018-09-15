__all__ = ['State']
from enum import Enum
class State(Enum):
    PENDING = 0
    READY = 1
    RUNNING = 2
    COMPLETED = 3
    FAILED = 4
