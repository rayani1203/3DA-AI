from typing import List
from .Card import *
from .Cards import *
from .Ante import Ante
from .Flight import Flight
from .AIPlayer import AIPlayer
from .Player import Player
from collections import defaultdict

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
    
    # def simulateTurn(self, prev: Value) -> Card:

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
        return self.AIPlayer.gold + sum(card.coinValue for card in self.AIPlayer.cards)
    