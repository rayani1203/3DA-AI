from .Flight import Flight
from .Card import *
from .Cards import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.TDA import TDA

class Player:
    def __init__(self, gold: int, cardCount: int=6):
        self.gold = gold
        self.cardCount = cardCount
        self.flight = Flight()
    
    def playTurn(self, prev: Value, game: "TDA") -> Card:
        while True:
            cardInput = input("please enter the card they played\n")
            try:
                [colorInput, valueInput] = cardInput.split(" ")
                color = Color(colorInput.capitalize())
                value = Value(int(valueInput))
                thisCard: Card = COLOR_TO_CLASS[color](value)
                self.cardCount -= 1
                self.flight.addCard(thisCard)
                if thisCard.value.value <= prev.value:
                    thisCard.power(self, game.players)
                return thisCard
            except:
                print("Invalid input, try again\n")
    
    def simTurn(self, prev: Value, game: "TDA") -> Card:
        nextCard = self.determineNext(game)
        self.cardCount -= 1
        self.flight.addCard(nextCard)
        if nextCard.value.value <= prev.value:
            nextCard.power(self, game.players)
        return nextCard

    def determineNext(self, game: "TDA") -> Card:

    
    """TODO: remove gold / hole"""
