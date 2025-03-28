from typing import List, TYPE_CHECKING
from .Card import *
from .Ante import Ante
import game.Flight as Flight
from MCTS.MCTS import MCTS
from copy import deepcopy

if TYPE_CHECKING:
    from .TDA import TDA

class AIPlayer:
    def __init__(self, gold: int, cards: List[Card]):
        self.gold = gold
        self.cards = cards
        self.flight = Flight.Flight()
        self.MCTS = MCTS(100000, 20)
    
    def ante(self, game: "TDA"):
        anteMCTS = MCTS(100000, 9)
        thisGame = deepcopy(game)
        thisGame.turn = thisGame.numPlayers - 1
        outcomes = []
        thisGame.AIPlayer.cards.sort(key=lambda x: x.value.value)
        cardsToCheck = thisGame.AIPlayer.cards[:len(thisGame.AIPlayer.cards)//2 + 1]
        print(cardsToCheck)
        for card in cardsToCheck:
            ante = []
            thisGame.AIPlayer.cards.remove(card)
            ante.append(card)
            for player in thisGame.players:
                ante.append(player.determineAnte())
                player.cardCount -= 1
            thisGame.ante = Ante(ante)
            outcomes.append((card, anteMCTS.search(thisGame)[1]))
            thisGame.AIPlayer.cards.append(card)
            for player in thisGame.players:
                player.cardCount += 1
        outcomes.sort(key=lambda x: x[1], reverse=True)
        anteCard = outcomes[0][0]
        for card in self.cards:
            if card.color == anteCard.color and card.value == anteCard.value:
                self.cards.remove(card)
                break
        print(f"\n\n **** AI ADVICE: ante {anteCard.color.value} {anteCard.value.value}\n")
        return anteCard
    
    def playTurn(self, game: "TDA", prev: Value) -> Card:
        if len(self.cards) <= 1:
            (payment, cards) = game.buyCards(3, False, True)
            self.gold -= payment
            self.cards += cards
        playCard = self.MCTS.search(game)[0]
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
        initLen = len(self.cards)
        print(f"Looking for {chosen.color} {chosen.value}")
        for card in self.cards:
            print(f"Card {card.color} {card.value}")
            if card.value == chosen.value and card.color == chosen.color:
                self.cards.remove(card)
                break
        assert len(self.cards) == initLen - 1
        self.flight.addCard(chosen, game.ante, self, True)
        if chosen.value.value <= prev.value:
            chosen.power(self, game, True)
        return chosen
    
    def decideCard(self, game: "TDA", value: Value, above: bool, isSim: bool = False):
        """***TODO*** decide card / coin"""
        options = []
        if not isSim:
            decisionMCTS = MCTS(100000, 10)
            self.gold -= 5
            res2 = decisionMCTS.search(game)
            self.gold += 5
        for card in self.cards:
            if (card.value.value > value.value and above and card.good) or (card.value.value < value.value and not above and not card.good):
                if isSim:
                    options.append((card, 13-card.value.value))
                else:
                    self.cards.remove(card)
                    res1 = decisionMCTS.search(game)
                    self.cards.append(card)
                    if res1[1] > res2[1]:
                        options.append((card, res1[1]))
        if options:
            options.sort(key=lambda x: x[1], reverse=True)
            chosen = options[0][0]
            self.cards.remove(chosen)
            print(f"**** AI ADVICE: give card {chosen.color.value} {chosen.value.value}")

            if len(self.cards) == 0:
                if not isSim:
                    (payment, cards) = game.buyCards(4, False, True)
                else:
                    (payment, cards) = game.buyCards(4, True)
                self.gold -= payment
                self.cards += cards
            
            return chosen
        print("**** AI ADVICE: give coins, not card")
        self.gold -= 5
        return None
