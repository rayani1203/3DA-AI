from typing import List
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
    
    @abstractmethod
    def power(self):
        pass

# Subclasses for each color
class GoldCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Gold, value)
        self.good = True
    
    def power(self):
        pass

class SilverCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Silver, value)
        self.good = True
    
    def power(self):
        pass

class CopperCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Copper, value)
        self.good = True
    
    def power(self):
        pass

class BronzeCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Bronze, value)
        self.good = True
    
    def power(self):
        pass

class BrassCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Brass, value)
        self.good = True
    
    def power(self):
        pass

class RedCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Red, value)
        self.good = False
    
    def power(self):
        pass

class BlackCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Black, value)
        self.good = False
    
    def power(self):
        pass

class GreenCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Green, value)
        self.good = False
    
    def power(self):
        pass

class WhiteCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.White, value)
        self.good = False
    
    def power(self):
        pass

class BlueCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Blue, value)
        self.good = False
    
    def power(self):
        pass

COLOR_TO_CLASS = {
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
            if player.cardCount < 3:
                return False
            sums.append(player.flight.total)
        sums.sort()
        return sums[-1] > sums[-2]

    def playAnte(self):
        thisAnteCards: List[Card] = []
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
        
        thisAnteCards.append(self.AIPlayer.ante(self))
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
        return idx

    def playTurn(self):
        self.printStatus()
        """*******TODO********"""
        input()
    
    def printStatus(self):
        print('this is where we play a turn')
        print('state:')
        print('ante:')
        print(self.ante.cards)
        print(self.ante.value)
        print(f"turn: {self.turn}")
        print(f"cards: {self.AIPlayer.cards}, gold: {self.AIPlayer.gold}")
        for i, player in enumerate(self.players):
            print(f"{i}: {player.cardCount}, {player.gold}")

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

class Player:
    def __init__(self, gold: int, cardCount: int=6):
        self.gold = gold
        self.cardCount = cardCount
        self.flight = Flight()

class AIPlayer:
    def __init__(self, gold: int, cards: List[Card]):
        self.gold = gold
        self.cards = cards
        self.flight = Flight()
    
    def ante(self, game: TDA):
        anteCard = min(self.cards, key=lambda card:card.value.value)
        self.cards.remove(anteCard)
        return anteCard
        

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
        while not game.isGambitOver():
            game.playTurn()
    
    """***TODO****"""


play_game()