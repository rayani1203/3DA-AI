from typing import List
from Card import Card

class Flight:
    def __init__(self):
        self.cards: List[Card] = []
        self.total = 0
        self.goods = 0
        self.evils = 0
    
    def addCard(self, card: Card):
        self.cards.append(card)
        self.total += card.value.value
        if card.good:
            self.goods += 1
        else:
            self.evils += 1        