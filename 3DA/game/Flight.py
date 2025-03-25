from typing import List, Union
from .Card import *
from .Ante import Ante
import game.Player as Player
import game.AIPlayer as AIPlayer
from collections import defaultdict

class Flight:
    def __init__(self):
        self.cards: List[Card] = []
        self.total = 0
        self.goods = 0
        self.evils = 0
        self.value_count = defaultdict(int)
    
    def addCard(self, card: Card, ante: Ante, player: Union[Player.Player, AIPlayer.AIPlayer], isSim: bool = False):
        self.cards.append(card)
        self.total += card.value.value
        if card.good:
            self.goods += 1
        else:
            self.evils += 1   
        self.value_count[card.value.value] += 1
        if self.value_count[card.value.value] == 3:
            goldToAdd = card.value.value
            player.gold += goldToAdd
            ante.value -= min(goldToAdd, ante.value)
        
            cardsToAdd = min(2, len(ante.cards))
            removed_cards = []
            if not isSim:
                for _ in range(cardsToAdd):
                    while True:
                        card_input = input("Enter a card to remove from ante (format: Color Value):\n")
                        try:
                            color_input, value_input = card_input.split(" ")
                            color = Color(color_input.capitalize())
                            value = Value(int(value_input))
                            card_to_remove = next((c for c in ante.cards if c.color == color and c.value == value), None)
                            if card_to_remove:
                                ante.cards.remove(card_to_remove)
                                removed_cards.append(card_to_remove)
                                break
                            else:
                                print("Card not found in ante. Try again.")
                        except Exception as e:
                            print(f"Invalid input, try again. Exception: {e}")
            else:
                ante.cards.sort(key=lambda c: c.value.value, reverse=True)
                removed_cards = ante.cards[:cardsToAdd]
                ante.cards = ante.cards[cardsToAdd:]
            if isinstance(player, AIPlayer.AIPlayer):    
                player.cards += removed_cards
            else:
                player.cardCount += cardsToAdd