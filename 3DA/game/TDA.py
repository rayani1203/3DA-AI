from typing import List
from .Card import *
import game.Cards as Cards
from .Ante import Ante
from .Flight import Flight
from .AIPlayer import AIPlayer
from .Player import Player
from collections import defaultdict
import random

class TDA:
    def __init__(self, numPlayers: int, playerGold: int, AICards: List[Card]):
        self.numPlayers = numPlayers
        self.players: List[Player]= []
        for _ in range(numPlayers-1):
            self.players.append(Player(playerGold*numPlayers))
        self.AIPlayer = AIPlayer(playerGold*numPlayers, AICards)
        self.ante: Ante = None
        self.turn: int = None
        self.prev = Value(13)
        self.playerGold = playerGold
    
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
                thisAnteCards.append(Cards.COLOR_TO_CLASS[color](value))
                self.players[len(thisAnteCards)-1].cardCount -= 1
            except Exception as e:
                print(f"Invalid input, try again\nexception: {e}")
        
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
                    self.AIPlayer.cards.append(Cards.COLOR_TO_CLASS[color](value))
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
        thisRound : List[Card] = [None] * self.numPlayers
        self.prev = Value(13)
        while turns < self.numPlayers:
            playedCard = self.playTurn()
            self.prev = playedCard.value
            turns += 1
            thisRound[self.turn] = playedCard
            self.turn = (self.turn + 1)%self.numPlayers
        newStart = self.findStart(thisRound)
        if newStart != -1:
            self.turn = newStart
    
    def playTurn(self) -> Card:
        if self.turn != self.numPlayers-1:
            print(f"Player {self.turn} turn...")
            newPrev = self.players[self.turn].playTurn(self.prev, self)
        else:
            newPrev = self.AIPlayer.playTurn(self, self.prev)
        return newPrev

    def simTurn(self, choice: Card):
        if all(len(player.flight.cards) > 0 for player in self.players) and len(self.AIPlayer.flight.cards) > 0:
            if all(len(player.flight.cards) == len(self.players[0].flight.cards) for player in self.players) and len(self.AIPlayer.flight.cards) == len(self.players[0].flight.cards):
                newStart = self.findStart([player.flight.cards[-1] for player in self.players] + [self.AIPlayer.flight.cards[-1]])
                if newStart != -1:
                    self.turn = newStart
                    self.prev = Value(13)
        print(f"simulating turn for player {self.turn}...")
        if self.turn == self.numPlayers-1:
            used = self.AIPlayer.simTurn(self, self.prev, choice)
        else:
            used = self.players[self.turn].simTurn(self.prev, self)
        self.turn = (self.turn + 1)%self.numPlayers
        self.prev = used.value
        
    def doColorFlights(self):
        toRemove = 0
        for player in self.players:
            color_counts = defaultdict(lambda: {'count': 0, 'values': []})
            for card in player.flight.cards:
                color_counts[card.color]['count'] += 1
                color_counts[card.color]['values'].append(card.value.value)
            for color, props in color_counts.items():
                if props['count'] >= 3:
                    props['values'].sort()
                    flightVal = props['values'][1]
                    player.gold += flightVal*self.numPlayers
                    toRemove += flightVal
                
        color_counts = defaultdict(lambda: {'count': 0, 'values': []})
        for card in self.AIPlayer.flight.cards:
            color_counts[card.color]['count'] += 1
            color_counts[card.color]['values'].append(card.value.value)
        for color, props in color_counts.items():
            if props['count'] >= 3:
                props['values'].sort()
                flightVal = props['values'][1]
                self.AIPlayer.gold += flightVal*self.numPlayers
                toRemove += flightVal
        
        for player in self.players:
            player.gold -= toRemove
        self.AIPlayer.gold -= toRemove

    def endGambit(self):
        self.doColorFlights()

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
                    thisCard: Card = Cards.COLOR_TO_CLASS[color](value)
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
        if self.ante:
            print('ante:')
            print(self.ante.cards)
            print(self.ante.value)
            print(f"turn: {self.turn}")
        print(f"cards: {self.AIPlayer.cards}, gold: {self.AIPlayer.gold}")
        for i, player in enumerate(self.players):
            print(f"{i}: {player.cardCount}, {player.gold}")
        print()

    def getGameScore(self):
        """***TODO***"""
        return self.AIPlayer.gold + sum(card.coinValue for card in self.AIPlayer.cards)
    
    def buyCards(self, num: int = 3, isSim: bool = False):
        if not isSim:
            while True:
                try:
                    payment = int(input("Need to BUY. Enter how much to buy for: "))
                    if 1 <= payment <= 13:
                        break
                    else:
                        print("Please enter a valid number between 1 and 13.")
                except ValueError:
                    print("Invalid input. Please enter an integer.")
            cards = []
            for _ in range(num):
                while True:
                    try:
                        color = input("Enter card color: ").capitalize()
                        value = int(input("Enter card value: "))
                        cards.append(Card(Color(color), Value(value)))
                        break
                    except Exception as e:
                        print(f"Invalid input. Error: {e}")
        else:
            payment = random.randint(1, 13)
            cards = []
            for _ in range(num):
                color = random.choice(list(Cards.COLOR_TO_CLASS.keys()))
                value = random.randint(1, 13)
                cards.append(Cards.COLOR_TO_CLASS[color](Value(value)))
        return (payment, cards)