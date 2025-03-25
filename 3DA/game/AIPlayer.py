from typing import List, TYPE_CHECKING
from .Card import *
import game.Flight as Flight
from MCTS.MCTS import MCTS

if TYPE_CHECKING:
    from .TDA import TDA

class AIPlayer:
    def __init__(self, gold: int, cards: List[Card]):
        self.gold = gold
        self.cards = cards
        self.flight = Flight.Flight()
        self.MCTS = MCTS(100000, 20)
    
    def ante(self, game: "TDA"):
        """***TODO***"""
        anteCard = min(self.cards, key=lambda card:card.value.value)
        self.cards.remove(anteCard)
        print(f"\n\n **** AI ADVICE: ante {anteCard.color.value} {anteCard.value.value}\n")
        return anteCard
    
    def playTurn(self, game: "TDA", prev: Value) -> Card:
        if len(self.cards) <= 1:
            (payment, cards) = game.buyCards()
            self.gold -= payment
            self.cards += cards
        playCard = self.MCTS.search(game)
        print(f"\n\n AI player's turn...\n***** AI ADVICE: play {playCard.color.value} {playCard.value.value}\n")
        prevAmount = len(self.cards)
        for card in self.cards:
            if card.color == playCard.color and card.value == playCard.value:
                self.cards.remove(card)
                break
        assert len(self.cards) == prevAmount - 1
        self.flight.addCard(playCard, game.ante, self)
        if playCard.value.value <= prev.value:
            playCard.power(self, game)
        return playCard

    def simTurn(self, game: "TDA", prev: Value, chosen: Card) -> Card:
        if len(self.cards) <= 1:
            (payment, cards) = game.buyCards(4-len(self.cards), True)
            self.gold -= payment
            self.cards += cards
        for card in self.cards:
            if card.value == chosen.value and card.color == chosen.color:
                self.cards.remove(card)
                break
        self.flight.addCard(chosen, game.ante, self, True)
        if chosen.value.value <= prev.value:
            chosen.power(self, game, True)
        return chosen
    
    def decideCard(self, game: "TDA", value: Value, above: bool, isSim: bool = False):
        """***TODO*** decide card / coin"""
        for card in self.cards:
            if card.value.value > value.value and above and card.good:
                print(f"**** AI ADVICE: give card {card.color.value} {card.value.value}")
                self.cards.remove(card)
                if len(self.cards) == 0:
                    if not isSim:
                        (payment, cards) = game.buyCards(4)
                    else:
                        (payment, cards) = game.buyCards(4, True)
                    self.gold -= payment
                    self.cards += cards
                return card
            elif card.value.value < value.value and not above and not card.good:
                print(f"**** AI ADVICE: give card {card.color.value} {card.value.value}")
                self.cards.remove(card)
                if len(self.cards) == 0:
                    if not isSim:
                        (payment, cards) = game.buyCards(4)
                    else:
                        (payment, cards) = game.buyCards(4, True)
                    self.gold -= payment
                    self.cards += cards
                return card
        
        print("**** AI ADVICE: give coins, not card")
        self.gold -= 5
        return None

    """TODO: remove gold / hole"""    
