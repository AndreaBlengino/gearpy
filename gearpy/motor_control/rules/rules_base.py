from abc import ABC, abstractmethod


class RuleBase(ABC):

    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    def apply(self): ...
