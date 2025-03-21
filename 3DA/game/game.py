from typing import List
from Card import *
from Cards import *
from TDA import TDA

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