from typing import List, TYPE_CHECKING
from .Card import *
from .Flight import Flight
from MCTS.MCTS import MCTS

if TYPE_CHECKING:
    from .TDA import TDA

class AIPlayer:
    def __init__(self, gold: int, cards: List[Card]):
        self.gold = gold
        self.cards = cards
        self.flight = Flight()
        self.MCTS = MCTS(100000, 20)
    
    def ante(self, game: "TDA"):
        """***TODO***"""
        anteCard = min(self.cards, key=lambda card:card.value.value)
        self.cards.remove(anteCard)
        print(f"\n\n **** AI ADVICE: ante {anteCard.color.value} {anteCard.value.value}\n")
        return anteCard
    
    def playTurn(self, game: "TDA", prev: Value) -> Card:
        playCard = self.MCTS.search(game, prev)
        self.cards.pop(0)
        self.flight.addCard(playCard)
        if playCard.value.value <= prev.value:
            playCard.power(self, game)
        print(f"\n\n AI player's turn...\n***** AI ADVICE: play {playCard.color.value} {playCard.value.value}\n")
        return playCard

    def simTurn(self, game: "TDA", prev: Value, chosen: Card) -> Card:
        for card in self.cards:
            if card.value == chosen.value and card.color == chosen.color:
                self.cards.remove(card)
                break
        self.flight.addCard(chosen)
        if chosen.value.value <= prev.value:
            chosen.power(self, game, True)
        return chosen
    
    def decideCard(self, game: "TDA", value: Value, above: bool):
        """***TODO*** decide card / coin"""
        for card in self.cards:
            if card.value.value > value.value and above and card.good:
                print(f"**** AI ADVICE: give card {card.color.value} {card.value.value}")
                self.cards.remove(card)
                return card
            elif card.value.value < value.value and not above and not card.good:
                print(f"**** AI ADVICE: give card {card.color.value} {card.value.value}")
                self.cards.remove(card)
                return card
        
        print("**** AI ADVICE: give coins, not card")
        self.gold -= 5
        return None

    """TODO: remove gold / hole"""    
