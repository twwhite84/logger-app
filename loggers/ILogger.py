from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Dict


class StatusType(Enum):
    SUCCESS = 1
    WARNING = 2
    FAILURE = 3


class ILogger(metaclass=ABCMeta):
    @abstractmethod
    def log(self, logdata: Dict[str, str], status_type: StatusType) -> None:
        pass
