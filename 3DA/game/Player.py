import game.Flight as Flight
from .Card import *
import game.Cards as Cards
from typing import TYPE_CHECKING
import random
import math

if TYPE_CHECKING:
    from .TDA import TDA


class Player:
    def __init__(self, gold: int, cardCount: int=6):
        self.gold = gold
        self.cardCount = cardCount
        self.flight = Flight.Flight()
        self.NumToProb = {
            1: 0.0090,
            2: 0.0218,
            3: 0.0448,
            4: 0.0784,
            5: 0.1169,
            6: 0.1486,
            7: 0.1610,
            8: 0.1486,
            9: 0.1169,
            10: 0.0784,
            11: 0.0448,
            12: 0.0218,
            13: 0.0090
        }
    
    def playTurn(self, prev: Value, game: "TDA") -> Card:
        if self.cardCount <= 1:
            (payment, cards) = game.buyCards()
            self.gold -= payment
            self.cardCount += len(cards)
        while True:
            cardInput = input("please enter the card they played\n")
            try:
                [colorInput, valueInput] = cardInput.split(" ")
                color = Color(colorInput.capitalize())
                value = Value(int(valueInput))
                thisCard: Card = Cards.COLOR_TO_CLASS[color](value)
                self.cardCount -= 1
                self.flight.addCard(thisCard, game.ante, self)
                self.bayesianUpdate()
                if thisCard.value.value <= prev.value:
                    thisCard.power(self, game)
                return thisCard
            except Exception as e:
                print(f"Invalid input, try again\nError: {e}")
    
    def simTurn(self, prev: Value, game: "TDA") -> Card:
        if self.cardCount <= 1:
            (payment, cards) = game.buyCards((4-self.cardCount), True)
            self.gold -= payment
            self.cardCount += len(cards)
        nextCard = self.determineNext()
        self.cardCount -= 1
        self.flight.addCard(nextCard, game.ante, self, True)
        if nextCard.value.value <= prev.value:
            nextCard.power(self, game, True)
        return nextCard

    def determineNext(self) -> Card:
        predictedVal = random.choices(list(self.NumToProb.keys()), weights=self.NumToProb.values(), k=1)[0]
        predictedColorClass = random.choice(list(Cards.COLOR_TO_CLASS.values()))
        predictedCard = predictedColorClass(Value(predictedVal))
        return predictedCard

    def bayesianUpdate(self):
        stdDev = 2.7-(len(self.flight.cards)*0.5)
        posts = []
        for prev in self.NumToProb:
            prevProb = self.NumToProb[prev]
            likelihood = math.exp(-((prev - (self.flight.cards[-1].value.value - 1)) ** 2)/(2*(stdDev**2)))
            unnormPost = prevProb * likelihood
            posts.append(unnormPost)
        norm = sum(posts)
        for i in range(len(posts)):
            self.NumToProb[i+1] = posts[i]/norm
        
        print(self.NumToProb)
