from typing import Union
from .Card import *
from .TDA import TDA
from .Player import Player
from .AIPlayer import AIPlayer
import random

def randomCard():
    color = random.choice(list(Color))
    value = random.choice(list(Value))
    return COLOR_TO_CLASS[color](value)

# Subclasses for each color
class GoldCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Gold, value)
        self.good = True
    
    def power(self, player: Union["Player", "AIPlayer"], game: TDA, isSim : bool = False):
        print(f"{self.color} dragon triggers...")
        print(f"Receiving {player.flight.goods} cards")
        if isinstance(player, Player):
            player.cardCount += player.flight.goods
        else:
            cardsReceived = player.flight.goods
            for _ in range(cardsReceived):
                if not isSim:
                    cardInput = input("Enter a card to add to AI player's hand:\n")
                    try:
                        colorInput, valueInput = cardInput.split(" ")
                        color = Color(colorInput.capitalize())
                        value = Value(int(valueInput))
                        newCard = COLOR_TO_CLASS[color](value)
                        player.cards.append(newCard)
                    except Exception:
                        print("Invalid input, try again\n")
                else:
                    player.cards.append(randomCard())

class SilverCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Silver, value)
        self.good = True
    
    def power(self, player: Union["Player", "AIPlayer"], game: TDA, isSim : bool = False):
        print(f"{self.color} dragon triggers...")
        for p in game.players:
            if p.flight.goods > 0:
                p.cardCount += 1
        if game.AIPlayer.flight.goods > 0:
            if not isSim:
                while True:
                    cardInput = input("Enter a card to add to AI player's hand:\n")
                    try:
                        colorInput, valueInput = cardInput.split(" ")
                        color = Color(colorInput.capitalize())
                        value = Value(int(valueInput))
                        newCard = COLOR_TO_CLASS[color](value)
                        game.AIPlayer.cards.append(newCard)
                        break
                    except Exception:
                        print("Invalid input, try again\n")
            else:
                game.AIPlayer.cards.append(randomCard())

class CopperCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Copper, value)
        self.good = True
    
    def power(self, player: Union["Player", "AIPlayer"], game: TDA, isSim : bool = False):
        print(f"{self.color} dragon triggers...")
        if not isSim:
            while True:
                cardInput = input("Enter the card that is drawn from the deck:\n")
                try:
                    colorInput, valueInput = cardInput.split(" ")
                    color = Color(colorInput.capitalize())
                    value = Value(int(valueInput))
                    newCard: Card = COLOR_TO_CLASS[color](value)
                    break
                except Exception:
                    print("Invalid input, try again\n")
        else:
            newCard = randomCard()
        player.flight.cards.pop(-1)
        player.flight.addCard(newCard)
        newCard.power(player, game, isSim)

class BronzeCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Bronze, value)
        self.good = True
    
    def power(self, player: Union["Player", "AIPlayer"], game: TDA, isSim : bool = False):
        print(f"{self.color} dragon triggers...")
        anteCards = game.ante.cards
        anteCards.sort(key=lambda card: card.value.value)
        cards = 0
        drawnCards = []
        while cards < 2 and anteCards:
            drawnCards.append(anteCards.pop(0))
            cards += 1
        if isinstance(player, Player):
            player.cardCount += len(drawnCards)
        else:
            player.cards.extend(drawnCards)

class BrassCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Brass, value)
        self.good = True
    
    def power(self, player: Union["Player", "AIPlayer"], game: TDA, isSim : bool = False):
        print(f"{self.color} dragon triggers...")
        toAI = False
        if isinstance(player, AIPlayer):
            idx = -1
            toAI = True
        else:
            idx = 0
            for i, p in enumerate(game.players):
                if player == p:
                    idx = i
                    break
            if idx == 0:
                card = game.AIPlayer.decideCard(game, self.value, True)
                if card:
                    player.cardCount += 1
                else:
                    player.gold += 5
                return
            else:
                idx -= 1
        if not isSim:
            (gives, card) = card_coin_choice(game.players[idx], game, self.value, True, toAI)
        else:
            gives = random.choice([True, False])
            card = randomCard()
        if gives:
            if isinstance(player, Player):
                player.cardCount += 1
            else:
                player.cards.append(card)
        else:
            player.gold += 5

class RedCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Red, value)
        self.good = False
    
    def power(self, player: Union["Player", "AIPlayer"], game: TDA, isSim : bool = False):
        print(f"{self.color} dragon triggers...")
        highest = -1
        biggest = []
        for i, opp in enumerate(game.players):
            if opp == player:
                continue
            if opp.flight.total > highest:
                highest = opp.flight.total
                biggest = [i]
            elif opp.flight.total == highest:
                biggest.append(i)
        if isinstance(player, Player):
            if game.AIPlayer.flight.total > highest:
                biggest = [game.numPlayers - 1]
            elif game.AIPlayer.flight.total == highest:
                biggest.append(game.numPlayers - 1)
        if len(biggest) > 1:
            if not isSim:
                while True:
                    try:
                        selectedOpp = int(input(f"Player must select which opponent to draw from\noptions: {biggest}"))
                        break
                    except:
                        print("Invalid input, enter an integer")
            else:
                selectedOpp = random.choice(biggest)
        else:
            selectedOpp = biggest[0]
        if selectedOpp < game.numPlayers - 1:
            game.players[selectedOpp].gold -= 1
            game.players[selectedOpp].cardCount -= 1
        else:
            game.AIPlayer.gold -= 1
            print("Drawing from AI...")
            if not isSim:
                while True:
                    cardInput = input("Enter the card drawn from AI player's hand:\n")
                    try:
                        colorInput, valueInput = cardInput.split(" ")
                        color = Color(colorInput.capitalize())
                        value = Value(int(valueInput))
                        cardToRemove = next(card for card in game.AIPlayer.cards if card.color == color and card.value == value)
                        game.AIPlayer.cards.remove(cardToRemove)
                        break
                    except StopIteration:
                        print("Card not found in AI player's hand, try again\n")
                    except Exception:
                        print("Invalid input, try again\n")
            else:
                game.AIPlayer.cards.remove(random.choice(game.AIPlayer.cards))

        player.gold += 1
        if isinstance(player, Player):
            player.cardCount += 1
        else:
            if not isSim:
                while True:
                    cardInput = input("Enter the card added to the AI player's hand:\n")
                    try:
                        colorInput, valueInput = cardInput.split(" ")
                        color = Color(colorInput.capitalize())
                        value = Value(int(valueInput))
                        player.cards.append(COLOR_TO_CLASS[color](value))
                        break
                    except:
                        print("Invalid input, try again\n")
            else:
                player.cards.append(randomCard())

class BlackCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Black, value)
        self.good = False
    
    def power(self, player: Union["Player", "AIPlayer"], game: TDA, isSim : bool = False):
        print(f"{self.color} dragon triggers...")
        amount = min(3, game.ante.value)
        game.ante.value -= amount
        player.gold += amount

class GreenCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Green, value)
        self.good = False
    
    def power(self, player: Union["Player", "AIPlayer"], game: TDA, isSim : bool = False):
        print(f"{self.color} dragon triggers...")
        toAI = False
        if isinstance(player, AIPlayer):
            idx = 0
            toAI = True
        else:
            idx = 0
            for i, p in enumerate(game.players):
                if player == p:
                    idx = i
                    break
            if idx == len(game.players)-1:
                card = game.AIPlayer.decideCard(game, self.value, False)
                if card:
                    player.cardCount += 1
                else:
                    player.gold += 5
                return
            else:
                idx += 1
        if not isSim:
            (gives, card) = card_coin_choice(game.players[idx], game, self.value, False, toAI)
        else:
            gives = random.choice([True, False])
            card = randomCard()
        if gives:
            if isinstance(player, Player):
                player.cardCount += 1
            else:
                player.cards.append(card)
        else:
            player.gold += 5

class WhiteCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.White, value)
        self.good = False
    
    def power(self, player: Union["Player", "AIPlayer"], game: TDA, isSim : bool = False):
        print(f"{self.color} dragon triggers...")
        weakest = float('inf')
        weakest_opponents = []
        for i, opp in enumerate(game.players):
            if opp == player:
                continue
            if opp.flight.total < weakest:
                weakest = opp.flight.total
                weakest_opponents = [i]
            elif opp.flight.total == weakest:
                weakest_opponents.append(i)
        if isinstance(player, Player):
            if game.AIPlayer.flight.total < weakest:
                weakest_opponents = [game.numPlayers - 1]
            elif game.AIPlayer.flight.total == weakest:
                weakest_opponents.append(game.numPlayers - 1)
        if len(weakest_opponents) > 1:
            if not isSim:
                while True:
                    try:
                        selectedOpp = int(input(f"Player must select which opponent to draw from\noptions: {weakest_opponents}"))
                        break
                    except:
                        print("Invalid input, enter an integer")
            else:
                selectedOpp = random.choice(weakest_opponents)
        else:
            selectedOpp = weakest_opponents[0]
        if selectedOpp < game.numPlayers - 1:
            game.players[selectedOpp].gold -= 2
        else:
            game.AIPlayer.gold -= 2

        player.gold += 2

class BlueCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Blue, value)
        self.good = False
    
    def power(self, player: Union["Player", "AIPlayer"], game: TDA, isSim : bool = False):
        print(f"{self.color} dragon triggers...")
        if not isSim:
            while True:
                addAnteInput = input("Option: Enter 'Y' if you would like to add money to the stakes, and 'N' if you'd like 1 from each opponent")
                if addAnteInput.capitalize() == 'Y':
                    addAnte = True
                elif addAnteInput.capitalize() == 'N':
                    addAnte = False
                else:
                    continue
                break
        else:
            addAnte = random.choice([True, False])
        if addAnte:
            amount = len(player.flight.cards)
            for opp in game.players:
                if opp == player:
                    continue
                opp.gold -= amount
                game.ante.value += amount
            if isinstance(player, Player):
                game.AIPlayer.gold -= amount
                game.ante.value += amount
        else:
            for opp in game.players:
                opp.gold -= 1
                player.gold += 1
            game.AIPlayer.gold -= 1
            player.gold += 1

COLOR_TO_CLASS: Card = {
    Color.Gold: GoldCard,
    Color.Silver: SilverCard,
    Color.Copper: CopperCard,
    Color.Bronze: BronzeCard,
    Color.Brass: BrassCard,
    Color.Red: RedCard,
    Color.Black: BlackCard,
    Color.Green: GreenCard,
    Color.White: WhiteCard,
    Color.Blue: BlueCard,
}

def card_coin_choice(receiver: Union[Player, AIPlayer], game:TDA, value: Value, above: bool, toAI: bool):
    if isinstance(receiver, AIPlayer):
        return receiver.decideCard(game, value, above)
    else:
        choice = input("Would you like to give a card? (Y/N)\n").strip().upper()
        if choice == 'Y':
            if toAI:
                while True:
                    cardInput = input("Enter the card to give:\n")
                    try:
                        colorInput, valueInput = cardInput.split(" ")
                        color = Color(colorInput.capitalize())
                        value = Value(int(valueInput))
                        cardToGive = COLOR_TO_CLASS[color](value)
                        receiver.cardCount -= 1
                        return (True, cardToGive)
                    except StopIteration:
                        print("Card not found in player's hand, try again\n")
                    except Exception:
                        print("Invalid input, try again\n")
            else:
                receiver.cardCount -= 1
                return (True, None)
        else:
            receiver.gold -= 5
            return (False, None)
