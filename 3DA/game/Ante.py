from typing import List
from Card import Card

class Ante:
    def __init__(self, cards: List[Card]):
        self.cards = cards
        self.anteValue = max(cards, key=lambda card:card.value.value).value.value
        self.value = self.anteValue*len(cards)