from enum import Enum
from abc import ABC, abstractmethod

class Color(Enum):
    Gold = "Gold"
    Silver = "Silver"
    Copper = "Copper"
    Bronze = "Bronze"
    Brass = "Brass"
    Red = "Red"
    Black = "Black"
    Green = "Green"
    White = "White"
    Blue = "Blue"

class Value(Enum):
    One = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Eleven = 11
    Twelve = 12
    Thirteen = 13

class Card(ABC):
    def __init__(self, color: Color, value: Value):
        self.color = color
        self.value = value
        self.good = None
    
    @abstractmethod
    def power(self, player):
        pass