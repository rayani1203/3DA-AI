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

class Player:
    def __init__(self, gold: int, cardCount: int=6):
        self.gold = gold
        self.cardCount = cardCount
        self.flight = Flight()
    
    def playTurn(self, prev: Value) -> Card:
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
                    thisCard.power(self)
                return thisCard
            except:
                print("Invalid input, try again\n")

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
            newPrev = self.players[self.turn].playTurn(prev)
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
            playCard.power(self)
        print(f"\n\n AI player's turn...\n***** AI ADVICE: play {playCard.color.value} {playCard.value.value}\n")
        return playCard
    
# Subclasses for each color
class GoldCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Gold, value)
        self.good = True
    
    def power(self, player: Union[Player, AIPlayer]):
        pass

class SilverCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Silver, value)
        self.good = True
    
    def power(self, player: Union[Player, AIPlayer]):
        pass

class CopperCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Copper, value)
        self.good = True
    
    def power(self, player: Union[Player, AIPlayer]):
        pass

class BronzeCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Bronze, value)
        self.good = True
    
    def power(self, player: Union[Player, AIPlayer]):
        pass

class BrassCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Brass, value)
        self.good = True
    
    def power(self, player: Union[Player, AIPlayer]):
        pass

class RedCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Red, value)
        self.good = False
    
    def power(self, player: Union[Player, AIPlayer]):
        pass

class BlackCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Black, value)
        self.good = False
    
    def power(self, player: Union[Player, AIPlayer]):
        pass

class GreenCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Green, value)
        self.good = False
    
    def power(self, player: Union[Player, AIPlayer]):
        pass

class WhiteCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.White, value)
        self.good = False
    
    def power(self, player: Union[Player, AIPlayer]):
        pass

class BlueCard(Card):
    def __init__(self, value: Value):
        super().__init__(Color.Blue, value)
        self.good = False
    
    def power(self, player: Union[Player, AIPlayer]):
        pass

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