from typing import List, Union
from enum import Enum
from abc import ABC, abstractmethod
from collections import defaultdict

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

# Subclasses for each color
class GoldCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Gold, value)
        self.good = True
    
    def power(self, player: Union["Player", "AIPlayer"], game: "TDA"):
        print(f"{self.color} dragon triggers...")
        print(f"Receiving {player.flight.goods} cards")
        if isinstance(player, Player):
            player.cardCount += player.flight.goods
        else:
            cardsReceived = player.flight.goods
            for _ in range(cardsReceived):
                cardInput = input("Enter a card to add to AI player's hand:\n")
                try:
                    colorInput, valueInput = cardInput.split(" ")
                    color = Color(colorInput.capitalize())
                    value = Value(int(valueInput))
                    newCard = COLOR_TO_CLASS[color](value)
                    player.cards.append(newCard)
                except Exception:
                    print("Invalid input, try again\n")

class SilverCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Silver, value)
        self.good = True
    
    def power(self, player: Union["Player", "AIPlayer"], game: "TDA"):
        print(f"{self.color} dragon triggers...")
        for p in game.players:
            if p.flight.goods > 0:
                p.cardCount += 1
        if game.AIPlayer.flight.goods > 0:
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

class CopperCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Copper, value)
        self.good = True
    
    def power(self, player: Union["Player", "AIPlayer"], game: "TDA"):
        print(f"{self.color} dragon triggers...")
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
        newCard.power(player, game)

class BronzeCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Bronze, value)
        self.good = True
    
    def power(self, player: Union["Player", "AIPlayer"], game: "TDA"):
        print(f"{self.color} dragon triggers...")
        anteCards = game.ante.cards
        anteCards.sort(key=lambda card: card.value)
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
    
    def power(self, player: Union["Player", "AIPlayer"], game: "TDA"):
        print(f"{self.color} dragon triggers...")
        pass

class RedCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Red, value)
        self.good = False
    
    def power(self, player: Union["Player", "AIPlayer"], game: "TDA"):
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
        while True and len(biggest) > 1:
            try:
                selectedOpp = int(input(f"Player must select which opponent to draw from\noptions: {biggest}"))
                break
            except:
                print("Invalid input, enter an integer")
        if selectedOpp < game.numPlayers - 1:
            game.players[selectedOpp].gold -= 1
            game.players[selectedOpp].cardCount -= 1
        else:
            game.AIPlayer.gold -= 1
            print("Drawing from AI...")
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

        player.gold += 1
        if isinstance(player, Player):
            player.cardCount += 1
        else:
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

class BlackCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Black, value)
        self.good = False
    
    def power(self, player: Union["Player", "AIPlayer"], game: "TDA"):
        print(f"{self.color} dragon triggers...")
        amount = min(3, game.ante.value)
        game.ante.value -= amount
        player.gold += amount

class GreenCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Green, value)
        self.good = False
    
    def power(self, player: Union["Player", "AIPlayer"], game: "TDA"):
        print(f"{self.color} dragon triggers...")
        pass

class WhiteCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.White, value)
        self.good = False
    
    def power(self, player: Union["Player", "AIPlayer"], game: "TDA"):
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
        while True and len(weakest_opponents) > 1:
            try:
                selectedOpp = int(input(f"Player must select which opponent to draw from\noptions: {weakest_opponents}"))
                break
            except:
                print("Invalid input, enter an integer")
        if selectedOpp < game.numPlayers - 1:
            game.players[selectedOpp].gold -= 2
        else:
            game.AIPlayer.gold -= 2

        player.gold += 2

class BlueCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Blue, value)
        self.good = False
    
    def power(self, player: Union["Player", "AIPlayer"], game: "TDA"):
        print(f"{self.color} dragon triggers...")
        while True:
            addAnteInput = input("Option: Enter 'Y' if you would like to add money to the stakes, and 'N' if you'd like 1 from each opponent")
            if addAnteInput.capitalize() == 'Y':
                addAnte = True
            elif addAnteInput.capitalize() == 'N':
                addAnte = False
            else:
                continue
            break
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

class TDA:
    def __init__(self, numPlayers: int, playerGold: int, AICards: List[Card]):
        self.numPlayers = numPlayers
        self.players: List[Player]= []
        for _ in range(numPlayers-1):
            self.players.append(Player(playerGold*numPlayers))
        self.AIPlayer = AIPlayer(playerGold*numPlayers, AICards)
        self.ante: Ante = None
        self.turn: int = None
    
    def isGameOver(self):
        return min(self.players, key=lambda player:player.gold).gold < 0

    def isGambitOver(self):
        if len(self.AIPlayer.flight.cards) < 3:
            return False
        sums = [self.AIPlayer.flight.total]
        for player in self.players:
            sums.append(player.flight.total)
        sums.sort()
        return sums[-1] > sums[-2]

    def playAnte(self):
        thisAnteCards: List[Card] = []
        AIAnte = self.AIPlayer.ante(self)
        while len(thisAnteCards) < self.numPlayers - 1:
            cardInput = input(f"Please enter player {len(thisAnteCards)} ante card in standard format (\"Color Value\")\n")
            try:
                [colorInput, valueInput] = cardInput.split(" ")
                color = Color(colorInput.capitalize())
                value = Value(int(valueInput))
                thisAnteCards.append(COLOR_TO_CLASS[color](value))
                self.players[len(thisAnteCards)-1].cardCount -= 1
            except:
                print("Invalid input, try again\n")
        
        thisAnteCards.append(AIAnte)
        startIdx = self.findStart(thisAnteCards)
        if startIdx == -1:
            for player in self.players:
                player.cardCount += 1
            print("The ante is a tie!!!")
            while True:
                newCard = input('Please enter the new card for AI\n')
                try:
                    [colorInput, valueInput] = newCard.split(" ")
                    color = Color(colorInput.capitalize())
                    value = Value(int(valueInput))
                    self.AIPlayer.cards.append(COLOR_TO_CLASS[color](value))
                    break
                except:
                    print("Invalid input, try again\n")
            self.playAnte()
            return

        self.ante = Ante(thisAnteCards)

        for player in self.players:
            player.gold -= self.ante.anteValue
        
        self.AIPlayer.gold -= self.ante.anteValue

        self.turn = startIdx

        print("Ante completed successfully\n\n")
    
    def findStart(self, cards: List[Card]):
        counts = defaultdict(int)
        for card in cards:
            counts[card.value.value] += 1
        idx = -1
        highest = 0
        for i, card in enumerate(cards):
            if card.value.value > highest and counts[card.value.value] == 1:
                idx = i
                highest = card.value.value
        return idx

    def playRound(self, roundNum: int):
        print(f"Beginning round {roundNum}, starting with player {self.turn}")
        turns = 0
        prevVal = Value.Thirteen
        thisRound : List[Card] = [None] * self.numPlayers
        while turns < self.numPlayers:
            playedCard = self.playTurn(prevVal)
            prevVal = playedCard.value
            turns += 1
            thisRound[self.turn] = playedCard
            self.turn = (self.turn + 1)%self.numPlayers
        newStart = self.findStart(thisRound)
        if newStart != -1:
            self.turn = newStart
    
    def playTurn(self, prev: Value) -> Card:
        if self.turn != self.numPlayers-1:
            print(f"Player {self.turn} turn...")
            newPrev = self.players[self.turn].playTurn(prev, self)
        else:
            newPrev = self.AIPlayer.playTurn(self, prev)
        return newPrev

    def endGambit(self):
        print()

        winner = None
        highest = 0
        for player in self.players:
            if player.flight.total > highest:
                winner = player
                highest = player.flight.total
            player.flight = Flight()
        if self.AIPlayer.flight.total > highest:
            winner = self.AIPlayer
            print("AI won!!!")
        else:
            print("AI did not win...")
        self.AIPlayer.flight = Flight()
        winner.gold += self.ante.value

        self.ante = None

        self.printStatus()
    
    def dealCards(self):
        for player in self.players:
            player.cardCount = min(10, player.cardCount + 2)
        AICards = min(2, 10-len(self.AIPlayer.cards))
        for _ in range(AICards):
            while True:
                cardInput = input("Enter card dealt for new gambit to AI...\n")
                try:
                    [colorInput, valueInput] = cardInput.split(" ")
                    color = Color(colorInput.capitalize())
                    value = Value(int(valueInput))
                    thisCard: Card = COLOR_TO_CLASS[color](value)
                    self.AIPlayer.cards.append(thisCard)
                    break
                except Exception as e:
                    print(e)
                    print("Invalid input, try again\n")
    
    def checkWinner(self):
        highest = 0
        winner = -1
        for i, player in enumerate(self.players):
            if player.gold > highest:
                winner = i
                highest = player.gold
        
        if self.AIPlayer.gold >= highest:
            print(f"AI won with {self.AIPlayer.gold} gold!!!")
        else:
            print(f"Player {winner} won with {highest} gold")
    
    def printStatus(self):
        print('\nPRINTING current game status...\n')
        print('ante:')
        if self.ante:
            print(self.ante.cards)
            print(self.ante.value)
            print(f"turn: {self.turn}")
        print(f"cards: {self.AIPlayer.cards}, gold: {self.AIPlayer.gold}")
        for i, player in enumerate(self.players):
            print(f"{i}: {player.cardCount}, {player.gold}")
        print()

class Ante:
    def __init__(self, cards: List[Card]):
        self.cards = cards
        self.anteValue = max(cards, key=lambda card:card.value.value).value.value
        self.value = self.anteValue*len(cards)

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
    
    """TODO: remove gold / hole"""

class AIPlayer:
    def __init__(self, gold: int, cards: List[Card]):
        self.gold = gold
        self.cards = cards
        self.flight = Flight()
    
    def ante(self, game: TDA):
        """***TODO***"""
        anteCard = min(self.cards, key=lambda card:card.value.value)
        self.cards.remove(anteCard)
        print(f"\n\n **** AI ADVICE: ante {anteCard.color.value} {anteCard.value.value}\n")
        return anteCard
    
    def playTurn(self, game: TDA, prev: Value) -> Card:
        "***TODO***"
        playCard = self.cards[0]
        self.cards.pop(0)
        self.flight.addCard(playCard)
        if playCard.value.value <= prev.value:
            playCard.power(self, game.players)
        print(f"\n\n AI player's turn...\n***** AI ADVICE: play {playCard.color.value} {playCard.value.value}\n")
        return playCard  

    """TODO: remove gold / hole"""     

def play_game():
    print("*** WELCOME to 3DA AI ***\n\n")
    while True:
        try:
            numPlayers = int(input("Enter the number of players\n"))
            playerGold = int(input("Enter gold per person\n"))
            break
        except:
            print("Invalid input, try again\n")
    
    print("Deal cards, then input the 6 cards dealt to AI in the following format:\nColor Value\nex. \"Gold 9\"")
    AICards: List[Card] = []
    while len(AICards) < 6:
        cardInput = input()
        try:
            [colorInput, valueInput] = cardInput.split(" ")
            color = Color(colorInput.capitalize())
            value = Value(int(valueInput))
            AICards.append(COLOR_TO_CLASS[color](value))
        except:
            print("Invalid input, try again\n")
    
    game = TDA(numPlayers, playerGold, AICards)

    while not game.isGameOver():
        game.playAnte()
        round = 1
        while not game.isGambitOver():
            game.playRound(round)
            round += 1
        game.endGambit()
        game.dealCards()
    
    print("Game over...")
    print(game.checkWinner())

play_game()